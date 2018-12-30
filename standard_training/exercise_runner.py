from typing import List
import time

from rlbot.training.training import Pass, Fail, Exercise, run_all_exercises
from .grading import Grader, GraderExercise, CompoundGrader, FailOnTimeout
from rlbot.utils.logging_utils import get_logger

LOGGER_ID = 'training'

def infinite_seed_generator():
    yield 4
    while True:
        yield int(time.time() * 1000)

def run_exercises(exercises: List[GraderExercise], infinite=False):
    logger = get_logger(LOGGER_ID)

    seeds = [4]
    if infinite:
        logger.info('Running execises repeatedly until Ctrl+C is pressed...')
        seeds = infinite_seed_generator()

    result_iter = run_all_exercises(exercises, seeds=seeds)
    for name, result in result_iter:
        grade = result.grade
        if isinstance(grade, Pass):
            logger.info(f'{name}: {grade}')
        else:
            logger.warn(f'{name}: {grade}')
        # TODO: put result.exercise.get_metrics() into a database
