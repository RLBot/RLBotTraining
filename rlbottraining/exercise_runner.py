from types import ModuleType
from typing import Dict, Tuple, Iterator, Optional
import time
import traceback
from pathlib import Path
import importlib

from rlbot.setup_manager import SetupManager, setup_manager_context
from rlbot.training.training import Pass, run_exercises as _run_exercises, Result as _Result
from rlbot.utils.logging_utils import get_logger
from rlbot.utils.class_importer import load_external_module

from rlbottraining.training_exercise import TrainingExercise, Playlist
from rlbottraining.training_exercise_adapter import TrainingExerciseAdapter
from rlbottraining.history.exercise_result import ExerciseResult
from rlbottraining.history.reproducable_exercise import make_reproducable

LOGGER_ID = 'training'


def run_playlist(exercises: Playlist, history_dir: Optional[Path] = None, seed: int = 4) -> Iterator[ExerciseResult]:
    with setup_manager_context() as setup_manager:
        yield from _run_playlist(setup_manager, exercises, history_dir, seed)

def _run_playlist(setup_manager: SetupManager, exercises: Playlist, history_dir: Optional[Path], seed: int) -> Iterator[ExerciseResult]:
    wrapped_exercises = [
        TrainingExerciseAdapter(ex, make_reproducable(ex, seed, history_dir))
        for ex in exercises
    ]
    for result in _run_exercises(setup_manager, wrapped_exercises, seed):
        yield TrainingExerciseAdapter.unwrap_result(result)

class ReloadPolicy:
    NEVER = 1
    EACH_EXERCISE = 2
    # TODO: on .py file change in (sub-) directory

def run_module(python_file_with_playlist: Path, history_dir: Optional[Path] = None, reload_policy=ReloadPolicy.EACH_EXERCISE):
    """
    This method repeatedly runs exercises in the module and reloads the module to pick up
    any new changes to the Exercise. e.g. make_game_state() can be updated or
    you could implement a new Grader without needing to terminate the training.
    """
    playlist = load_default_exercises(python_file_with_playlist)
    should_restart_training = True
    seeds = infinite_seed_generator()
    with setup_manager_context() as setup_manager:
        while True:
            result_iter = _run_playlist(setup_manager, playlist, history_dir, next(seeds))
            for result in result_iter:
                print_result(result)
                # TODO write result to disk

                # Reload the module and apply the new exercises
                if reload_policy == ReloadPolicy.EACH_EXERCISE:
                    try:
                        new_playlist = load_default_exercises(python_file_with_playlist)
                    except Exception:
                        traceback.print_exc()
                        continue  # keep running previous exercises until new ones are fixed.
                    if len(new_playlist) != len(playlist) or any(e1.name != e2.name for e1,e2 in zip(new_playlist, playlist)):
                        get_logger(LOGGER_ID).warn(f'Need to restart to pick up new exercises.')
                        exercises = new_playlist
                        break  # different set of exercises. Can't monkeypatch.
                    for new_exercise, old_exercise in zip(new_playlist, playlist):
                        _monkeypatch_copy(new_exercise, old_exercise)

def infinite_seed_generator():
    yield 4
    while True:
        yield int(time.time() * 1000)

def print_result(result: ExerciseResult):
    grade = result.grade
    if isinstance(grade, Pass):
        get_logger(LOGGER_ID).info(f'{result.exercise.name}: {grade}')
    else:
        get_logger(LOGGER_ID).warn(f'{result.exercise.name}: {grade}')

def load_default_exercises(python_file_with_playlist: Path) -> Playlist:
    module = load_external_module(python_file_with_playlist)
    assert hasattr(module, 'make_default_playlist'), f'module "{python_file_with_playlist}" must provide a make_default_playlist() function to be able to used in run_module().'
    return module.make_default_playlist()

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
            continue  # ignore non-writable attributes like __weakref__.
