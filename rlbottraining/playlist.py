from typing import Dict

from .grading import GraderExercise

class Playlist:
    """
    A playlist is simply a container for exercises.
    Subclassing this is necessary to make your module compatible with run_module().
    """
    def make_exercises(self) -> Dict[str, GraderExercise]:
        raise NotImplementedError
