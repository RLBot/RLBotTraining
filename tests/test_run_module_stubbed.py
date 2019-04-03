from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Iterable, Iterator, List
import json
import unittest

from rlbot.setup_manager import SetupManager
from rlbot.training.training import Exercise as RLBotExercise, Grade, Result as RLBotResult, Pass, Fail

import rlbottraining.exercise_runner as exercise_runner
from rlbottraining.paths import HistoryPaths


testdata_dir = Path(__file__).absolute().parent / 'testdata'
testdata_module_v1 = testdata_dir / 'exercise_module_v1.py'
testdata_module_v2 = testdata_dir / 'exercise_module_v2.py'

@contextmanager
def fake_setup_manager_context():
    class FakeSetupManager:
        pass
    yield FakeSetupManager()

@dataclass
class FakeLogMessage:
    logger_name: str
    verbosity: str
    message: str

@dataclass
class FakeLogger:
    logger_name: str
    messages: List[FakeLogMessage]
    log_creation: bool = True

    def info(self, message: str):
        self.messages.append(FakeLogMessage(self.logger_name, 'info', message))
    def warning(self, message: str):
        self.messages.append(FakeLogMessage(self.logger_name, 'warning', message))

@contextmanager
def stub_out_rlbot(fake_rlbot_run_exercises: Callable) -> List[FakeLogMessage]:
    """
    stub out function calls in rlbot with fake ones.
    TODO: stub out logging
    returns
    """
    tmp_rlbot_run_exercises = exercise_runner.rlbot_run_exercises
    tmp_setup_manager_context = exercise_runner.setup_manager_context
    tmp_get_logger = exercise_runner.get_logger
    exercise_runner.setup_manager_context = fake_setup_manager_context
    exercise_runner.rlbot_run_exercises = fake_rlbot_run_exercises
    log_messages = []
    exercise_runner.get_logger = lambda logger_name: FakeLogger(logger_name, log_messages)
    try:
        yield log_messages
    finally:
        exercise_runner.setup_manager_context = tmp_setup_manager_context
        exercise_runner.rlbot_run_exercises = tmp_rlbot_run_exercises
        exercise_runner.get_logger = tmp_get_logger



class RunModuleTest(unittest.TestCase):
    """
    Tests the function that gets called in the `rlbottraining run_module` command.
    """

    def test_stubbed_run_module(self):
        class DeliberateExit(KeyboardInterrupt):
            pass

        with TemporaryDirectory(prefix='test_history_dir') as tmpdir:
            python_file_with_playlist = Path(tmpdir) / 'module_to_be_reloaded.py'
            with open(python_file_with_playlist, 'w') as f:
                f.write(testdata_module_v1.read_text())

            num_run_calls = 0
            def fake_rlbot_run_exercises(setup_manager: SetupManager, exercises: Iterable[RLBotExercise], seed: int) -> Iterator[RLBotResult]:
                nonlocal num_run_calls
                num_run_calls += 1
                if num_run_calls > 1:
                    raise DeliberateExit()
                exercises = iter(exercises)

                # The reloading should kick in after then first exercise.
                # Currently we are in a state where we have comitted to the
                # first exercise so the file-change-detection will happen after
                # we yield here and before we re-enter this function.
                with open(python_file_with_playlist, 'w') as f:
                    f.write(testdata_module_v2.read_text())

                yield RLBotResult(next(exercises), seed, Pass())
                yield RLBotResult(next(exercises), seed, Fail())


            with stub_out_rlbot(fake_rlbot_run_exercises) as log_messages:
                with self.assertRaises(DeliberateExit):
                    exercise_runner.run_module(python_file_with_playlist, history_dir=tmpdir)

            results_dir = tmpdir / HistoryPaths.exercise_results
            result_filepaths = list(results_dir.glob('*'))

            self.assertEqual(len(result_filepaths), 2)
            results = []
            for filepath in result_filepaths:
                with open(filepath) as f:
                    results.append(json.load(f))

            results.sort(key=lambda result: result['exercise']['name'])
            self.assertEqual(results[0]['exercise']['car_start_x'], 3.0)  # comes from original.
            self.assertEqual(results[1]['exercise']['car_start_x'], 6.0)  # comes from the reloaded file. (exercise_module_v2.py)
            self.assertTrue(results[0]['run_id'])
            self.assertTrue(results[1]['run_id'])
            self.assertNotEqual(results[0]['run_id'], results[1]['run_id'])
            self.assertEqual(
                results[0]['exercise']['__class__'],
                'rlbottraining.common_exercises.bronze_striker.FacingAwayFromBallInFrontOfGoal'
            )
            self.assertLess(
                results[0]['create_time']['iso8601'],
                results[1]['create_time']['iso8601'],
            )

            self.assertEqual(
                log_messages,
                [
                    FakeLogMessage(logger_name='training', verbosity='info', message='Facing away from ball [0]: PASS'),
                    FakeLogMessage(logger_name='training', verbosity='warning', message='Facing away from ball [1]: FAIL')
                ]
            )

if __name__ == '__main__':
    unittest.main()
