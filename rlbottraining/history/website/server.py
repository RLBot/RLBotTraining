import os
import json
from typing import List, Dict, Callable, Iterable
from dataclasses import dataclass, field
import shutil
from pathlib import Path

from rlbot.utils.class_importer import load_external_class

from rlbottraining.history.exercise_result import ExerciseResultJson
from rlbottraining.history.website.common_views.result_full_json import FullJsonAggregator
from rlbottraining.history.website.common_views.result_list import ResultListAggregator
from rlbottraining.history.website.view import Aggregator, Renderer
from rlbottraining.paths import HistoryPaths, _website_static_source

class Server:

    """
    This class manages the state of the views (renderers, website) given the authoritative data.
    It glues authoritative data, renderers, and the output website together.
    """

    history_dir: Path
    aggregators: List[Aggregator]
    url_map: Dict[Path, Renderer]

    def __init__(self, history_dir: Path, url_map: Dict[Path, Renderer]=None, aggregators: List[Aggregator]=None):
        self.history_dir = history_dir
        self.out_dir = self.history_dir / HistoryPaths.Website._website_dir
        self.url_map = {} if url_map is None else url_map

        if aggregators is None:
            aggregators = [
                FullJsonAggregator(shared_url_map=self.url_map),
                ResultListAggregator(shared_url_map=self.url_map),
                make_static_file_aggregator(_website_static_source)(shared_url_map=self.url_map),
            ]
        additional_aggregators_dir = history_dir / HistoryPaths.additional_website_code
        if additional_aggregators_dir.exists():
            assert additional_aggregators_dir.is_symlink(), f'{additional_aggregators_dir} should be a symlink'
            additional_aggregators_dir = additional_aggregators_dir.resolve(strict=True)
            for file in additional_aggregators_dir.iterdir():
                if not file.is_file:
                    continue  # ignore directories
                agg_class = load_external_class(file, Aggregator)
                aggregators.append(agg_class(shared_url_map=self.url_map))
        self.aggregators = aggregators

        input_dir = self.history_dir / HistoryPaths.exercise_results
        for result_json_file in input_dir.iterdir():
            with open(result_json_file) as f:
                self.add_exercise_result(json.load(f))


    def add_exercise_result(self, result_json: ExerciseResultJson):
        for agg in self.aggregators:
            agg.add_exercise_result(result_json)

    def render_static_website(self):
        self.clean_website()
        for path in self.url_map:
            self.render_to_disk(path)

    def clean_website(self):
        if self.out_dir.exists():
            shutil.rmtree(self.out_dir)

    def render_to_disk(self, path):
        renderer = self.url_map[path]
        file_path = self.out_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = renderer.render()
        if isinstance(content, bytes):
            file_path.write_bytes(content)
        else:
            file_path.write_text(content)

def make_static_file_aggregator(static_root: Path) -> type:
    class StaticFileAggregator(Aggregator):
        """
        Doesn't aggregate results at all, just adds renderers at creation time.
        These renderes just produce the content in the static files contained in static_root.
        """
        def __init__(self, shared_url_map: Dict[Path, Renderer]):
            super().__init__(shared_url_map)
            for root, dirs, files in os.walk(static_root):
                root = Path(root)
                for file in files:
                    path = root / file
                    serve_path = path.relative_to(static_root)
                    self.shared_url_map[serve_path] = StaticFileRenderer(file_path=path)
    return StaticFileAggregator

@dataclass
class StaticFileRenderer(Renderer):
    file_path: Path
    def render(self):
        return self.file_path.read_bytes()


def set_additional_website_code(additional_website_code: Path, history_dir: Path):
    """
    Ensures that the next time the server is started on history_dir,
    it will include the code in the provided files.
    """
    symlink_file = history_dir / HistoryPaths.additional_website_code
    if symlink_file.exists():
        symlink_file.remove()
    symlink_file.symlink_to(additional_website_code)
