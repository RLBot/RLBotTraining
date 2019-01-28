import random
import unittest
from dataclasses import dataclass, field
import tempfile
from pathlib import Path

from rlbot.training.training import Pass, Fail

from rlbottraining.common_graders.timeout import FailOnTimeout
from rlbottraining.paths import _common_exercises_dir
from rlbottraining.exercise_runner import run_playlist

class CommonExercisesTest(unittest.TestCase):
    '''
    This test runs common exercises with their default configs
    and checks that they perform as expected.
    '''

    def test_ball_prediction(self):
        from rlbottraining.common_exercises.ball_prediction import make_default_playlist
        results = list(run_playlist(make_default_playlist()))
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIsInstance(result.grade, Pass)

    def test_easy_striker(self):
        from rlbottraining.common_exercises.easy_striker import make_default_playlist
        result_iter = run_playlist(make_default_playlist())

        result = next(result_iter)
        self.assertEqual(result.exercise.name, 'Facing ball')
        self.assertIsInstance(result.grade, Pass)

        result = next(result_iter)
        self.assertEqual(result.exercise.name, 'Rolling Shot')
        self.assertIsInstance(result.grade, Pass)

        result = next(result_iter)
        self.assertEqual(result.exercise.name, 'Facing directly away from ball')
        self.assertIsInstance(result.grade, Fail)  # SimpleBot isn't smart enough.

        result = next(result_iter)
        self.assertEqual(result.exercise.name, 'Facing away from ball 1')
        self.assertIsInstance(result.grade, Pass)

        result = next(result_iter)
        self.assertEqual(result.exercise.name, 'Facing away from ball 2')
        self.assertIsInstance(result.grade, Pass)

        result = next(result_iter)
        self.assertEqual(result.exercise.name, 'Facing away from opponents goal')
        self.assertIsInstance(result.grade, FailOnTimeout.FailDueToTimeout)

        with self.assertRaises(StopIteration):
            next(result_iter)

        with self.assertRaises(StopIteration):
            next(result_iter)

if __name__ == '__main__':
    unittest.main()
