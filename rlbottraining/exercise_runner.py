from pathlib import Path
from types import ModuleType
from typing import Dict, Tuple, Iterator, Optional, Callable
import importlib
import time
import traceback
from contextlib import contextmanager

from rlbot.setup_manager import SetupManager, setup_manager_context
from rlbot.training.training import run_exercises as rlbot_run_exercises
from rlbot.utils.logging_utils import get_logger
from rlbot.utils.class_importer import load_external_module

from rlbottraining.training_exercise import TrainingExercise, Playlist
from rlbottraining.training_exercise_adapter import TrainingExerciseAdapter
from rlbottraining.history.exercise_result import ExerciseResult, ReproductionInfo, log_result, store_result

LOGGER_ID = 'training'

def run_playlist(playlist: Playlist, seed: int = 4, setup_manager: Optional[SetupManager]=None) -> Iterator[ExerciseResult]:
    """
    This function runs the given exercises in the playlist once and returns the result for each.
    """
    with use_or_create(setup_manager, setup_manager_context) as setup_manager:
        wrapped_exercises = [TrainingExerciseAdapter(ex) for ex in playlist]

        for i, rlbot_result in enumerate(rlbot_run_exercises(setup_manager, wrapped_exercises, seed)):
            yield ExerciseResult(
                grade=rlbot_result.grade,
                exercise=rlbot_result.exercise.exercise,  # unwrap the TrainingExerciseAdapter.
                reproduction_info=ReproductionInfo(
                    seed=seed,
                    playlist_index=i,
                )
            )

@contextmanager
def use_or_create(existing_context, default_contextmanager):
    if existing_context:
        yield existing_context
        return
    with default_contextmanager() as context:
        yield context

class ReloadPolicy:
    NEVER = 1
    EACH_EXERCISE = 2
    # TODO: on .py file change in (sub-) directory

def run_module(python_file_with_playlist: Path, history_dir: Optional[Path] = None, reload_policy=ReloadPolicy.EACH_EXERCISE):
    """
    This function repeatedly runs exercises in the module and reloads the module to pick up
    any new changes to the Exercise. e.g. make_game_state() can be updated or
    you could implement a new Grader without needing to terminate the training.
    """

    # load the playlist initially, keep trying if we fail
    playlist_factory = None
    playlist: Playlist = None
    while playlist is None:
        try:
            playlist_factory = load_default_playlist(python_file_with_playlist)
            playlist = playlist_factory()
        except Exception:
            traceback.print_exc()
            time.sleep(1.0)

    log = get_logger(LOGGER_ID)
    with setup_manager_context() as setup_manager:
        for seed in infinite_seed_generator():
            playlist = playlist_factory()
            wrapped_exercises = [TrainingExerciseAdapter(ex) for ex in playlist]
            result_iter = rlbot_run_exercises(setup_manager, wrapped_exercises, seed)

            for i, rlbot_result in enumerate(result_iter):
                result = ExerciseResult(
                    grade=rlbot_result.grade,
                    exercise=rlbot_result.exercise.exercise,  # unwrap the TrainingExerciseAdapter.
                    reproduction_info=ReproductionInfo(
                        seed=seed,
                        python_file_with_playlist=str(python_file_with_playlist.absolute()),
                        playlist_index=i,
                    )
                )

                log_result(result, log)
                if history_dir:
                    store_result(result, history_dir)

                # Reload the module and apply the new exercises
                if reload_policy == ReloadPolicy.EACH_EXERCISE:
                    try:
                        new_playlist_factory = load_default_playlist(python_file_with_playlist)
                        new_playlist = new_playlist_factory()
                    except Exception:
                        traceback.print_exc()
                        continue  # keep running previous exercises until new ones are fixed.
                    playlist_factory = new_playlist_factory
                    if len(new_playlist) != len(playlist) or any(e1.name != e2.name for e1,e2 in zip(new_playlist, playlist)):
                        log.warning(f'Need to restart to pick up new exercises.')
                        playlist = new_playlist
                        break  # different set of exercises. Can't monkeypatch.
                    for new_exercise, old_exercise in zip(new_playlist, playlist):
                        _monkeypatch_copy(new_exercise, old_exercise)


def infinite_seed_generator():
    yield 4
    while True:
        yield int(time.time() * 1000)


def load_default_playlist(python_file_with_playlist: Path) -> Callable[[], Playlist]:
    module = load_external_module(python_file_with_playlist)
    assert hasattr(module, 'make_default_playlist'), f'module "{python_file_with_playlist}" must provide a make_default_playlist() function to be able to used in run_module().'
    assert callable(module.make_default_playlist), 'make_default_playlist must be a function that returns TrainingExercise\'s'
    return module.make_default_playlist

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
