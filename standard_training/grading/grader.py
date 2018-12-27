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

class FailOnTimeout(Grader):
    """Fails the exercise if we take too long."""

    class FailDueToTimeout(Fail):
        pass

    def __init__(self, max_duration_seconds: float):
        self.max_duration_seconds = max_duration_seconds
        self.initial_seconds_elapsed: float = None
        self.measured_duration_seconds: float = None

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Grade]:
        seconds_elapsed = game_tick_packet.game_info.seconds_elapsed
        if self.initial_seconds_elapsed is None:
            self.initial_seconds_elapsed = seconds_elapsed
        self.measured_duration_seconds = seconds_elapsed - self.initial_seconds_elapsed
        if self.measured_duration_seconds > self.max_duration_seconds:
            return self.FailDueToTimeout()

    def get_metrics(self) -> Mapping[str, Any]:
        return {
            'max_duration_seconds': self.max_duration_seconds,
            'initial_seconds_elapsed': self.initial_seconds_elapsed,
            'measured_duration_seconds': self.measured_duration_seconds,
        }

def test_timeout():
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
    test_timeout()
