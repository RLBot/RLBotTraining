from typing import Any, Mapping, Optional

from rlbot.training.training import Grade

from . import TrainingTickPacket


class Grader:
    """
    A Grader is a part of an Exercise which judges the game states
    and makes decisions about whether to terminate.
    A Grader can optionally return implementation defined metrics.
    """

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        """ Similar to Exercise.on_tick() but takes a preprocessed data structure. """
        pass  # Continue by default

    def get_metrics(self) -> Mapping[str, Any]:
        return {}  # No metrics by default

