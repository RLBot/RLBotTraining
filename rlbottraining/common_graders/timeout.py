from typing import Any, Mapping, Optional
from dataclasses import dataclass

from rlbot.training.training import Pass, Fail, Grade

from rlbottraining.grading.grader import Grader, TrainingTickPacket
from rlbottraining.history.metric import Metric


class FailOnTimeout(Grader):
    """Fails the exercise if we take too long."""

    class FailDueToTimeout(Fail):
        def __init__(self, max_duration_seconds):
            self.max_duration_seconds = max_duration_seconds

        def __repr__(self):
            return f'{super().__repr__()}: Timeout: Took longer than {self.max_duration_seconds} seconds.'

    def __init__(self, max_duration_seconds: float):
        self.max_duration_seconds = max_duration_seconds
        self.initial_seconds_elapsed: float = None
        self.measured_duration_seconds: float = None

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        seconds_elapsed = tick.game_tick_packet.game_info.seconds_elapsed
        if self.initial_seconds_elapsed is None:
            self.initial_seconds_elapsed = seconds_elapsed
        self.measured_duration_seconds = seconds_elapsed - self.initial_seconds_elapsed
        if self.measured_duration_seconds > self.max_duration_seconds:
            return self.FailDueToTimeout(self.max_duration_seconds)

    @dataclass(frozen=True)
    class TimeoutMetric(Metric):
        max_duration_seconds: float
        initial_seconds_elapsed: float
        measured_duration_seconds: float
    def get_metric(self) -> Optional[Metric]:
        return FailOnTimeout.TimeoutMetric(
            self.max_duration_seconds,
            self.initial_seconds_elapsed,
            self.measured_duration_seconds,
        )


class PassOnTimeout(FailOnTimeout):
    """Passes the exercise if we manage not to fail until here."""

    class PassDueToTimeout(Pass):
        def __init__(self, max_duration_seconds):
            self.max_duration_seconds = max_duration_seconds

        def __repr__(self):
            return f'{super().__repr__()}: Timeout: Survived {self.max_duration_seconds} seconds.'

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        grade_maybe = super().on_tick(tick)
        if isinstance(grade_maybe, FailOnTimeout.FailDueToTimeout):
            grade_maybe = self.PassDueToTimeout(self.max_duration_seconds)
        return grade_maybe
