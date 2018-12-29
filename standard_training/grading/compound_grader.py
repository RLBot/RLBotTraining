from typing import Any, Mapping, Optional
from functools import reduce

from rlbot.training.training import Exercise, Pass, Fail, Grade
from rlbot.utils.structures.game_data_struct import GameTickPacket

from . import Grader


class CompoundGrader(Grader):
    """
    Combines a bunch of named Graders into one Grader which
    forwards calls to them.
    """

    def __init__(self, graders: Mapping[str, Grader]):
        self.graders = graders

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Grade]:
        grades = [ grader.on_tick(game_tick_packet) for grader in self.graders.values()]
        return reduce(pick_more_significant_grade, grades, None)

    def get_metrics(self) -> Mapping[str, Any]:
        return {
            grader_name: grader.get_metrics()
            for grader_name, grader in self.graders.items()
        }


def pick_more_significant_grade(a:Optional[Grade], b:Optional[Grade]) -> Optional[Grade]:
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
