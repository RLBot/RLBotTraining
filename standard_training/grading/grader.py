from typing import Any, Mapping, Optional
from functools import reduce

from rlbot.training.training import Exercise, Pass, Fail, Grade
from rlbot.utils.structures.game_data_struct import GameTickPacket, GameInfo

class Grader():
    """
    A Grader is a part of an Exercise which judges the game states
    and makes decisions about whether to terminate.
    A Grader can optionally return implementation defined metrics.
    """
    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Grade]:
        """ Similar to Exercise.on_tick() """
        pass # Continue by default
    def get_metrics(self) -> Mapping[str, Any]:
        return {}  # No metrics by default

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
    # Check assumptions that were made when writing this function
    assert a is None
    assert b is None
    return None
