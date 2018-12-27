from typing import Any, Mapping, Optional
from functools import reduce

from rlbot.training.training import Exercise, Pass, Fail, Grade
from rlbot.utils.structures.game_data_struct import GameTickPacket, GameInfo
from .grader import Grader

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
    # Check assumptions that were made when writing this function
    assert a is None
    assert b is None
    return None


def test_compound_grader():
    class TimeoutExercise(Exercise):
        def __init__(self):
            self.grader = CompoundGrader({
                'timeout': FailOnTimeout(3.5)
            })

        def on_tick(self, game_tick_packet):
            return self.grader.on_tick(game_tick_packet)

    def packet_with_time(time:float) -> GameTickPacket:
        return GameTickPacket(game_info=GameInfo(
            seconds_elapsed=time))

    ex = TimeoutExercise()
    assert ex.on_tick(packet_with_time(10)) is None
    assert ex.on_tick(packet_with_time(13.2)) is None
    fail_timeout = ex.on_tick(packet_with_time(13.6))
    assert fail_timeout is not None
    assert isinstance(fail_timeout, FailOnTimeout.FailDueToTimeout)

    ex = TimeoutExercise()
    assert ex.on_tick(packet_with_time(20)) is None
    assert ex.on_tick(packet_with_time(23.2)) is None
    fail_timeout = ex.on_tick(packet_with_time(23.6))
    assert fail_timeout is not None
    assert isinstance(fail_timeout, FailOnTimeout.FailDueToTimeout)


if __name__ == '__main__':
    test_compound_grader()
