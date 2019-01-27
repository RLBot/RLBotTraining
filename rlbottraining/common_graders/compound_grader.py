from dataclasses import dataclass
from functools import reduce
from typing import Optional, List

from rlbot.training.training import Pass, Fail, Grade
from rlbot.utils.rendering.rendering_manager import RenderingManager

from rlbottraining.grading.grader import Grader, TrainingTickPacket
from rlbottraining.history.metric import Metric


class CompoundGrader(Grader):
    """
    Combines a bunch of named Graders into one Grader which
    forwards calls to them.
    """

    def __init__(self, graders: List[Grader]):
        self.graders = graders

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        grades = [grader.on_tick(tick) for grader in self.graders]
        return reduce(pick_more_significant_grade, grades, None)

    def render(self, renderer: RenderingManager):
        for grader in self.graders:
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
