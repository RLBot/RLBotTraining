import json
from typing import List
from dataclasses import dataclass, field
from pathlib import Path

from rlbottraining.history.exercise_result import ExerciseResultJson
from rlbottraining.history.website.view import Aggregator, Renderer
from rlbottraining.paths import HistoryPaths

@dataclass
class FullJsonRenderer(Renderer):
    """
    Returns contents for static files which can be served.
    Usually for data from an aggregator.
    """
    result_json: ExerciseResultJson

    def render(self) -> str:
        return json.dumps(self.result_json)

@dataclass
class FullJsonAggregator(Aggregator):

    def add_exercise_result(self, result_json: ExerciseResultJson):
        path = HistoryPaths.Website.data_dir / 'result_json' / f'{result_json["run_id"]}.json'
        self.shared_url_map[path] = FullJsonRenderer(result_json=result_json)

