import time
from typing import Dict
import importlib
import traceback

from rlbot.training.training import Pass, run_all_exercises, Result
from rlbot.utils.logging_utils import get_logger

from .grading import GraderExercise

LOGGER_ID = 'training'


def infinite_seed_generator():
    yield 4
    while True:
        yield int(time.time() * 1000)

def on_result(name: str, result: Result):
    grade = result.grade
    if isinstance(grade, Pass):
        get_logger(LOGGER_ID).info(f'{name}: {grade}')
    else:
        get_logger(LOGGER_ID).warn(f'{name}: {grade}')


def run_exercises(exercises: Dict[str, GraderExercise], infinite=False):
    seeds = [4]
    if infinite:
        get_logger(LOGGER_ID).info('Running exercises repeatedly until Ctrl+C is pressed...')
        seeds = infinite_seed_generator()

    result_iter = run_all_exercises(exercises, seeds=seeds)
    for name, result in result_iter:
        on_result(name, result)
        # TODO: put result.exercise.get_metrics() into a database

def run_with_reloading(module):
    """
    This method runs exercises in the module and reloads the module to pick up
    any new changes to the Exercise. e.g. make_game_state() can be updated or
    you could implement a new Grader without needing to terminate the training.
    """
    assert hasattr(module, 'get_exercises'), 'The exercise module must provide a get_exercises() function which returns a Dict[str, GraderExercise].'

    while True:
        exercises = module.get_exercises()
        result_iter = run_all_exercises(exercises, seeds=infinite_seed_generator())
        for name, result in result_iter:
            on_result(name, result)

            # reload
            try:
                importlib.reload(module)
            except Exception:
                traceback.print_exc()
                continue
            new_exercises = module.get_exercises()
            if new_exercises.keys() != exercises.keys():
                get_logger(LOGGER_ID).warn(f'Need to restart to pick up new exercises.')
                break  # different set of exercises. Can't monkeypatch.
            for ex_name, old_exercise in exercises.items():
                _monkeypatch_copy(new_exercises[ex_name], old_exercise)

def _monkeypatch_copy(source, destination):
    """
    Mutates the destination object to behave like the source object.
    """
    for attr_name in dir(destination):
        if not hasattr(source, attr_name):
            delattr(destination, attr_name)
    for attr_name in dir(source):
        attr = getattr(source, attr_name)
        try:
            setattr(destination, attr_name, attr)
        except AttributeError:
            continue  # ignore non-writable ones attributes like __weakref__.
