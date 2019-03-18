import json
from typing import List
from dataclasses import dataclass, field
from pathlib import Path

from rlbottraining.history.exercise_result import ExerciseResultJson
from rlbottraining.history.website.json_utils import slim_copy
from rlbottraining.history.website.view import Aggregator, Renderer
from rlbottraining.paths import HistoryPaths

@dataclass
class SlimResultsRenderer(Renderer):
    """
    Returns contents for static files which can be served.
    Usually for data from an Aggregator.
    """
    slim_results: List[ExerciseResultJson]

    def render(self) -> str:
        return json.dumps(self.slim_results)


slim_keys = [path.split('.') for path in [
    '__class__',
    'run_id',
    'create_time',
    'exercise.name',
    'exercise.__class__',
    'exercise.grader.__class__',
    'grade.__class__',
    'grade.__isinstance_Pass__',
    'grade.__isinstance_Fail__',
]]

@dataclass
class ResultListAggregator(Aggregator):
    path: Path = field(default_factory=lambda: HistoryPaths.Website.data_dir/'slim_results.json')

    def add_exercise_result(self, result_json: ExerciseResultJson):
        if self.path in self.shared_url_map:
            renderer = self.shared_url_map[self.path]
            assert isinstance(renderer, SlimResultsRenderer)
        else:
            renderer = SlimResultsRenderer(slim_results=[])
        slim_result = slim_copy(result_json, slim_keys)
        renderer.slim_results.append(slim_result)
        self.shared_url_map[self.path] = renderer

