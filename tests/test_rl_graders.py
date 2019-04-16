from typing import Iterator, List
import unittest

from rlbot.training.training import Pass, Fail, FailDueToExerciseException

from rlbottraining.exercise_runner import run_playlist
from rlbottraining.history.exercise_result import ExerciseResult

class rl_grader_tester(unittest.TestCase):
    '''
    This tests the grader that simulates rocket league environments, like the shooter training pack
    '''

    def assertGrades(self, result_iter: Iterator[ExerciseResult], want_grades: List[str]):
        got_grades = []
        for result in result_iter:
            if isinstance(result.grade, FailDueToExerciseException):
                self.fail(str(result.grade))
                break
            got_grades.append(result.grade.__class__.__name__)
        self.assertEqual(got_grades, want_grades)

    def test_rl_graders(self):
        from tests.test_exercises.rl_grader_exercises import make_default_playlist
        self.assertGrades(
            run_playlist(make_default_playlist()),
            [
                'FailDueToGroundHit',
                #'FailDueToGroundHit',
                #'FailDueToTimeout',
             ]
        )

if __name__ == '__main__':
    unittest.main()
