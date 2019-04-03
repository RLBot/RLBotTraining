from typing import Iterator, List
from dataclasses import dataclass, field
from pathlib import Path
import random
import tempfile
import unittest

from rlbot.training.training import Pass, Fail, FailDueToExerciseException

from rlbot.training.training import Grade
from rlbottraining.common_graders.timeout import FailOnTimeout
from rlbottraining.exercise_runner import run_playlist
from rlbottraining.history.exercise_result import ExerciseResult
from rlbottraining.paths import _common_exercises_dir

class CommonExercisesTest(unittest.TestCase):
    '''
    This test runs common exercises with their default configs
    and checks that they perform as expected.
    '''

    def assertGrades(self, result_iter: Iterator[ExerciseResult], want_grades: List[str]):
        got_grades = []
        for result in result_iter:
            if isinstance(result.grade, FailDueToExerciseException):
                self.fail(str(result.grade))
                break
            got_grades.append(result.grade.__class__.__name__)
        self.assertEqual(got_grades, want_grades)

    # def test_ball_prediction(self):
    #     from rlbottraining.common_exercises.ball_prediction import make_default_playlist
    #     results = list(run_playlist(make_default_playlist()))
    #     self.assertEqual(len(results), 2)
    #     for result in results:
    #         self.assertIsInstance(result.grade, Pass)

    def test_bakkes_mod_import(self):
        from rlbottraining.common_exercises.bakkesmod_import.bakkesmod_importer import make_default_playlist
        playlist = make_default_playlist()
        assert len(playlist) > 2
        playlist = playlist[:2]  # for making tests run quicker
        results = list(run_playlist(playlist))
        self.assertEqual(len(results), 2)
        for result in results:
            # All of these exercises are too advanced for SimpleBot.
            self.assertIsInstance(result.grade, Fail)

    def assertNextGrade(self, result_iter: Iterator[ExerciseResult], expected_grade_class: type):
        result = next(result_iter)
        if not isinstance(result.grade, expected_grade_class):
            self.Fail(f'exercise "{result.exercise}" got a "{result.grade}" grade; want a {expected} grade.')


    def test_dribbling(self):
        from rlbottraining.common_exercises.dribbling import make_default_playlist
        self.assertGrades(
            run_playlist(make_default_playlist()),
            ['FailDueToTimeout']
        )

    def test_bronze_goalie(self):
        from rlbottraining.common_exercises.bronze_goalie import make_default_playlist
        self.assertGrades(
            run_playlist(make_default_playlist()),
            ['Pass']
        )

    def test_bronze_striker(self):
        from rlbottraining.common_exercises.bronze_striker import make_default_playlist
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

    def test_silver_goalie(self):
        from rlbottraining.common_exercises.silver_goalie import make_default_playlist
        self.assertGrades(
            run_playlist(make_default_playlist()),
            ['WrongGoalFail', 'WrongGoalFail', 'WrongGoalFail']
        )

    def test_silver_striker(self):
        from rlbottraining.common_exercises.silver_striker import make_default_playlist
        self.assertGrades(
            run_playlist(make_default_playlist()),
            ['FailDueToTimeout']
        )

    def test_wall_play(self):
        from rlbottraining.common_exercises.wall_play import make_default_playlist
        self.assertGrades(
            run_playlist(make_default_playlist()),
            ['FailDueToTimeout']
        )

    # # Commented out because RLBot has a bug where it doesn't like chaning the number of players.
    # def test_versus_line_goalie(self):
    #     from rlbottraining.common_exercises.versus_line_goalie import make_default_playlist
    #     self.assertGrades(
    #         run_playlist(make_default_playlist()),
    #         ['FailDueToTimeout', 'FailDueToTimeout']
    #     )

if __name__ == '__main__':
    unittest.main()
