from typing import List, Dict, Callable
import json

from contextlib import contextmanager
from pathlib import Path

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer
from rlbot.utils.logging_utils import get_logger

from rlbottraining.history.exercise_result import ExerciseResultJson
from rlbottraining.paths import HistoryPaths

logger = get_logger('server')

@contextmanager
def monitor_authoritative_data(history_dir: Path, incremental_callback: Callable[[ExerciseResultJson], None], reset_callback: Callable[[], None]):
    """
    Monitors the authoritative data within history_dir and signals when action needs to be taken.
    """
    event_handler = AuthoritativeDataMonitor(incremental_callback, reset_callback)
    observer = Observer()
    logger.debug('monitoring: ' + str(history_dir / HistoryPaths.authoritative_data))
    observer.schedule(event_handler, str(history_dir / HistoryPaths.authoritative_data), recursive=True)
    observer.start()
    yield
    observer.stop()
    observer.join()



class AuthoritativeDataMonitor(LoggingEventHandler):
    def __init__(
            self,
            incremental_callback: Callable[[ExerciseResultJson], None],
            reset_callback: Callable[[], None]):
        self.incremental_callback = incremental_callback
        self.reset_callback = reset_callback

    def on_created(self, event):
        pass

    def on_modified(self, event):
        if event.is_directory: return
        logger.warning(f'Authoritative data was written: {event.src_path}')
        assert event.src_path.endswith('.json')
        with open(event.src_path) as f:
            self.incremental_callback(json.load(f))

    def on_deleted(self, event):
        if event.is_directory: return
        logger.warning(f'{event.src_path} was deleted.')
        self.reset_callback()

    def on_moved(self, event):
        if event.is_directory: return
        logger.warning(f'{event.src_path} was moved.')
        self.reset_callback()
