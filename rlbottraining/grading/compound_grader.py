from functools import reduce
from typing import Any, Mapping, Optional

from rlbot.training.training import Pass, Fail, Grade
from rlbot.utils.rendering.rendering_manager import RenderingManager

from . import Grader, TrainingTickPacket


class CompoundGrader(Grader):
    """
    Combines a bunch of named Graders into one Grader which
    forwards calls to them.
    """

    def __init__(self, graders: Mapping[str, Grader]):
        self.graders = graders

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        grades = [grader.on_tick(tick) for grader in self.graders.values()]
        return reduce(pick_more_significant_grade, grades, None)

    def get_metrics(self) -> Mapping[str, Any]:
        return {
            grader_name: grader.get_metrics()
            for grader_name, grader in self.graders.items()
        }

    def render(self, renderer: RenderingManager):
        for grader in self.graders.values():
            grader.render(renderer)

def pick_more_significant_grade(a: Optional[Grade], b: Optional[Grade]) -> Optional[Grade]:
    """
    Chooses to return @a or @b based on some measure of sigificance.
    On equal significance, it favours @a.
    """
    if isinstance(a, Fail):
        return a
    elif isinstance(b, Fail):
        return b
    elif isinstance(a, Pass):
        return a
    elif isinstance(b, Pass):
        return b
    assert a is None, f'{type(a)} must inherit either from Pass or Fail'
    assert b is None, f'{type(b)} must inherit either from Pass or Fail'
    return None
