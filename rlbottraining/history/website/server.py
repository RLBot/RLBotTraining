import json
from typing import List, Dict
from dataclasses import dataclass, field
import shutil
from pathlib import Path

from rlbottraining.history.exercise_result import ExerciseResultJson
from rlbottraining.history.website.common_views.result_full_json import FullJsonAggregator
from rlbottraining.history.website.common_views.result_list import ResultListAggregator
from rlbottraining.history.website.view import Aggregator, Renderer
from rlbottraining.paths import HistoryPaths

class Server():

    history_dir: Path
    aggregators: List[Aggregator]
    url_map: Dict[Path, Renderer]

    def __init__(self, history_dir, url_map=None, aggregators=None):
        self.history_dir = history_dir
        self.url_map = {} if url_map is None else url_map
        if aggregators is None:
            aggregators = [
                FullJsonAggregator(shared_url_map=self.url_map),
                ResultListAggregator(shared_url_map=self.url_map),
            ]
        self.aggregators = aggregators

        input_dir = self.history_dir / HistoryPaths.exercise_results
        for result_json_file in input_dir.iterdir():
            with open(result_json_file) as f:
                self.add_exercise_result(json.load(f))

    # TODO: monitor authoritative_data

    def add_exercise_result(self, result_json: ExerciseResultJson):
        for agg in self.aggregators:
            agg.add_exercise_result(result_json)

    def generate_static_website(self):
        out_dir = self.history_dir / HistoryPaths.static_website_dir
        if out_dir.exists():
            shutil.rmtree(out_dir)
        for path, renderer in self.url_map.items():
            file_path = out_dir / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(renderer.render())
