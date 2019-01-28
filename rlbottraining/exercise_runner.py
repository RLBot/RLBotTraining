from types import ModuleType
from typing import Dict, Tuple, Iterator
import time
import traceback
from pathlib import Path
import importlib

from rlbot.training.training import Pass, run_exercises as _run_exercises, Result as _Result
from rlbot.utils.logging_utils import get_logger
from rlbot.utils.class_importer import load_external_class

from rlbottraining.training_exercise import TrainingExercise, Playlist

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


def run_playlist(exercises: Playlist, history_dir: Optional[Path] = None, seed: int = 4) -> Iterator[Result]:
    with setup_manager_context() as setup_manager:
        yield from _run_playlist(setup_manager, exercises, history_dir, seed)

def _run_playlist(setup_manager: SetupManager, exercises: Playlist, history_dir: Optional[Path], seed: int) -> Iterator[Result]:
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

def run_module(python_file_with_playlist: Path, reload_policy=ReloadPolicy.EACH_EXERCISE):
    """
    This method repeatedly runs exercises in the module and reloads the module to pick up
    any new changes to the Exercise. e.g. make_game_state() can be updated or
    you could implement a new Grader without needing to terminate the training.
    """
    exercises = make_exercises(python_file_with_playlist)
    should_restart_training = True
    while should_restart_training:
        should_restart_training = False

        result_iter = _rlbot_run_exercises(exercises, seeds=infinite_seed_generator())
        for name, result in result_iter:
            on_result(name, result)

            # Reload the module and apply the new exercises
            if reload_policy == ReloadPolicy.EACH_EXERCISE:
                try:
                    new_exercises = make_exercises(python_file_with_playlist)
                except Exception:
                    traceback.print_exc()
                    continue  # keep running previous exercises until new ones are fixed.
                if new_exercises.keys() != exercises.keys():
                    get_logger(LOGGER_ID).warn(f'Need to restart to pick up new exercises.')
                    should_restart_training = True
                    exercises = new_exercises
                    break  # different set of exercises. Can't monkeypatch.
                for ex_name, old_exercise in exercises.items():
                    _monkeypatch_copy(new_exercises[ex_name], old_exercise)

def make_exercises(python_file_with_playlist: Path) -> Dict[str, GraderExercise]:
    cls_module = load_external_class(python_file_with_playlist, Playlist)
    playlist: Playlist = cls_module[0]()
    return playlist.make_exercises()

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
