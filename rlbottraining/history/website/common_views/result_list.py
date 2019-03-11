import json
from typing import List
from dataclasses import dataclass, field
from pathlib import Path

from rlbottraining.history.exercise_result import ExerciseResultJson
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

def get_nested(obj: ExerciseResultJson, key_path: List[str]):
    try:
        for key in key_path:
            obj = obj[key]
    except KeyError:
        return None
    return obj
def set_nested(out_json, key_path: List[str], value):
    key, *remaining_key_path = key_path
    if len(remaining_key_path) == 0:
        out_json[key] = value
        return
    if key in out_json:
        subobject = out_json[key]
        assert isinstance(subobject, dict)
    else:
        subobject = {}
        out_json[key] = subobject
    set_nested(subobject, remaining_key_path, value)
def slim_copy(in_json: ExerciseResultJson, key_paths: List[List[str]]) -> ExerciseResultJson:
    """
    Returns a copy of @in_json where only paths
    specified by @keys_paths are copied.
    """
    out_json = {}
    for key_path in key_paths:
        value = get_nested(in_json, key_path)
        if value is None:
            continue
        set_nested(out_json, key_path, value)
    return out_json

slim_keys = [path.split('.') for path in [
    '__class__',
    'run_id',
    'create_time_utc_seconds',
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

