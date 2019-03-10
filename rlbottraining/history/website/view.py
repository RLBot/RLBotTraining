from dataclasses import dataclass, field
from typing import Dict
from pathlib import Path

from rlbot.utils.logging_utils import get_logger

from rlbottraining.history.exercise_result import ExerciseResultJson

"""
This file descibes the common interface for views which show data
about Exercise results.
Concrete classes are in the common_views directory.
"""

class Renderer:
    """
    Returns contents for static files which can be served.
    Usually for data from an aggregator.
    """

    def render(self) -> str:
        raise NotImplementedError()

@dataclass
class Aggregator:

    """
    Aggregates parsed json ExerciseResults and adds renderers for the
    aggregated data to the shared_url_map.
    """

    # A mapping shared between Aggregators to sort out who handles which path.
    # We don't allow dynamic handling of all paths in a directory as
    # we'd like to be able to statically render our website out fully.
    shared_url_map: Dict[Path, Renderer]

    def add_exercise_result(self, result_json: ExerciseResultJson):
        pass
