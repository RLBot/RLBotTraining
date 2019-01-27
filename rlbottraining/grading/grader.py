from typing import Any, Mapping, Optional

from rlbot.training.training import Grade
from rlbot.utils.rendering.rendering_manager import RenderingManager

from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.history.metric import Metric


class Grader(Metric):
    """
    A Grader is a part of an Exercise which judges the game states
    and makes decisions about whether to terminate.
    Fields of a Grader will be serialized via the Metrics.
    """

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        """ Similar to Exercise.on_tick() but takes a preprocessed data structure. """
        pass  # Continue by default

    def render(self, renderer: RenderingManager):
        """
        This method is called each tick to render exercise debug information.
        This method is called after on_tick() / grading.
        It is optional to override this method.
        """
        pass
