from typing import Any, Mapping, Optional

from rlbot.training.training import Grade
from rlbot.utils.rendering.rendering_manager import RenderingManager

from . import TrainingTickPacket
from ..metrics.metric import Metric


class Grader:
    """
    A Grader is a part of an Exercise which judges the game states
    and makes decisions about whether to terminate.
    A Grader can optionally return implementation defined metrics.
    """

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        """ Similar to Exercise.on_tick() but takes a preprocessed data structure. """
        pass  # Continue by default

    def get_metric(self) -> Optional[Metric]:
        return None  # No metrics by default

    def render(self, renderer: RenderingManager):
        """
        This method is called each tick to render exercise debug information.
        This method is called after on_tick() / grading.
        It is optional to override this method.
        """
        pass
