from dataclasses import dataclass, field
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Optional, Dict, Any
import uuid
import json

from rlbot.training.training import Grade, Pass

from rlbottraining.history.metric import Metric
from rlbottraining.history.metric_json_encoder import MetricJsonEncoder
from rlbottraining.paths import HistoryPaths
from rlbottraining.training_exercise import TrainingExercise

ExerciseResultJson = Dict[str, Any]

@dataclass
class ReproductionInfo(Metric):
    """
    Descibes how to reproduce (re-run) the exercise that gave the result
    """
    seed: int
    python_file_with_playlist: Optional[str] = None
    playlist_index: Optional[int] = None

@dataclass
class ExerciseResult(Metric):
    """
    Describes the outcome of a TrainingExercise run.
    """
    grade: Grade
    exercise: TrainingExercise
    reproduction_info: ReproductionInfo
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    create_time: datetime = field(default_factory=lambda: datetime.utcnow())


def log_result(result: ExerciseResult, log: Logger):
    grade = result.grade
    try:
        grade_str = str(result.grade)
    except Exception as e:
        log.error(f'Could not format grade: {e}')
        return

    if isinstance(grade, Pass):
        log.info(f'{result.exercise.name}: {grade_str}')
    else:
        log.warning(f'{result.exercise.name}: {grade_str}')

def store_result(result: ExerciseResult, history_dir: Path):
    """
    Writes the result to disk within the history_dir.
    """
    run_descriptors = history_dir / HistoryPaths.exercise_results
    run_descriptors.mkdir(parents=True, exist_ok=True)
    file_path = run_descriptors / (result.run_id + '.json')

    assert not file_path.exists(), "OMG, somehow got the same run_id twice, causing a clash in file names"

    with open(file_path, 'w') as f:
        json.dump(result, f, cls=MetricJsonEncoder, sort_keys=True)
