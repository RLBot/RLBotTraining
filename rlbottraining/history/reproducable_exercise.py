from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import pickle
import time

from rlbottraining.training_exercise import TrainingExercise


@dataclass
class ReproducableExercise:
    exercise: TrainingExercise
    seed: int
    create_epoch_ms: int


def make_reproducable(exercise: TrainingExercise, seed: int, history_dir: Optional[Path]) -> Optional[str]:
    """
    writes information to disk such that the training exercise can be reproduced later.
    Returns a reproduce_key which can be passed to reproduce_exercise() at a later point in time.
    Returns None if history_dir is not provided
    """
    if history_dir is None:
        return None

    create_epoch_ms = int(time.time() * 1000)
    reproduce_key = f'create_epoch_ms-{create_epoch_ms}'
    pickle_dir = history_dir / HistoryPaths.match_configs
    pickle_dir.mkdir(parents=True, exist_ok=True)
    file_path = pickle_dir / _make_file_name(reproduce_key)

    assert not file_name.exists(), "OMG, somehow got the same reproduce_key twice, causing a clash in file names"

    repreducable = ReproducableExercise(exercise=exercise, seed=seed, create_epoch_ms=create_epoch_ms)
    with open(file_name, 'wb') as f:
        pickle.dump(repreducable, f)

    return reproduce_key

def reproduce_exercise(reproduce_key: str, history_dir: Path):
    # TODO: look up in
    raise NotImplementedError()

def _make_file_name(reproduce_key: str):
    return f'{reproduce_key}.pickle'
