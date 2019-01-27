import random
import unittest
from dataclasses import dataclass, field
import tempfile
from pathlib import Path

from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket, GameInfo
from rlbot.training.training import Exercise as RLBotExercise

from rlbottraining.common_graders.compound_grader import CompoundGrader
from rlbottraining.common_graders.timeout import FailOnTimeout
from rlbottraining.grading.event_detector import PlayerEvent, PlayerEventDetector, PlayerEventType
from rlbottraining.grading.grader import Grader
from rlbottraining.training_exercise import TrainingExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise_adapter import TrainingExerciseAdapter

"""
This file is a unit test for the grading module which does not require RocketLeague to run.
"""

class GradingTest(unittest.TestCase):

    def test_timeout_ten(self):
        with tempfile.TemporaryDirectory() as tmp_history_dir:
            ex: RLBotExercise = TrainingExerciseAdapter(
                TimeoutExercise(name='time to test'),
                Path(tmp_history_dir)
            )
            self.assertIsInstance(ex.setup(random.Random(7)), GameState)
            self.assertIsNone(ex.on_tick(packet_with_time(10)))
            self.assertIsNone(ex.on_tick(packet_with_time(13.2)))
            fail_timeout = ex.on_tick(packet_with_time(13.75))
            self.assertIsNotNone(fail_timeout)
            self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)

            # Check that the config path and its contents look sane
            self.assertTrue(ex.get_config_path().startswith(tmp_history_dir))
            # note: The repeated call to get_config_path() is intentional.
            #       as it checks the hash_named_file.exists() branch in ensure_match_config_on_disk()
            with open(ex.get_config_path()) as f:
                json_str = f.read()
            self.assertIn('simple_bot.cfg', json_str)
            self.assertIn('"gravity": "Default"', json_str)
            self.assertIn('"match_length": "Unlimited"', json_str)

    # def test_timeout_twenty_with_metrics(self):
    #     ex = TimeoutExercise('')
    #     ex.setup(random.Random(7))
    #     self.assertIsNone(ex.grader.on_tick(packet_with_time(20)))
    #     self.assertIsNone(ex.grader.on_tick(packet_with_time(23.2)))
    #     fail_timeout = ex.grader.on_tick(packet_with_time(23.75))
    #     self.assertIsNotNone(fail_timeout)
    #     self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)

    #     self.assertEqual(
    #         ex.grader.get_metric(),
    #         CompoundGrader.CompoundMetric({
    #             'my_test_timeout': FailOnTimeout.TimeoutMetric(
    #                 max_duration_seconds = 3.5,
    #                 initial_seconds_elapsed = 20.0,
    #                 measured_duration_seconds = 3.75,
    #             )
    #         })
    #     )

    def test_player_events(self):
        detector = PlayerEventDetector()
        gtp = GameTickPacket()
        gtp.game_info.seconds_elapsed = 14.
        gtp.num_cars = 2
        gtp.game_cars[1].score_info.goals = 3
        self.assertListEqual(detector.detect_events(gtp), [])
        self.assertListEqual(detector.detect_events(gtp), [])
        gtp = GameTickPacket()
        gtp.game_info.seconds_elapsed = 15.
        gtp.num_cars = 2
        gtp.game_cars[1].score_info.goals = 5
        self.assertListEqual(detector.detect_events(gtp), [PlayerEvent(
            type=PlayerEventType.GOALS,
            player=gtp.game_cars[1],
            seconds_elapsed=15.,
        )])
        self.assertListEqual(detector.detect_events(gtp), [])

@dataclass
class TimeoutExercise(TrainingExercise):
    grader: Grader = field(
        default_factory=lambda: CompoundGrader([FailOnTimeout(3.5)])
    )
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState()



def packet_with_time(time: float) -> GameTickPacket:
    return GameTickPacket(game_info=GameInfo(seconds_elapsed=time))


if __name__ == '__main__':
    unittest.main()
