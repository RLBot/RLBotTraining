from typing import List

from rlbot.training.training import Pass, Fail, Exercise, run_all_exercises
from .grading import Grader, GraderExercise, CompoundGrader, FailOnTimeout
from rlbot.utils.logging_utils import get_logger

LOGGER_ID = 'training'

def run_exercises(exercises: List[GraderExercise]):
    logger = get_logger(LOGGER_ID)
    result_iter = run_all_exercises(exercises)
    for name, result in result_iter:
        grade = result.grade
        if isinstance(grade, Pass):
            logger.info(f'{name}: {grade}')
        else:
            logger.warn(f'{name}: {grade}')
        # TODO: put result.exercise.get_metrics() into a database
