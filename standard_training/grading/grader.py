from typing import Any, Mapping, Optional
from functools import reduce
import random

from rlbot.training.training import Grade, Exercise
from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket


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

class GraderExercise(Exercise):
    """
    The usuall base-class for Exercises in this repo.
    Only requires users of this class to specify constructur arguments
    and implement setup().
    """
    def __init__(self, config_path:str, grader: Grader):
        self.config_path = config_path
        self.grader = grader

    def on_tick(self, game_tick_packet):
        return self.grader.on_tick(game_tick_packet)

    def get_config_path(self) -> str:
        return self.config_path

    def setup(self, rng: random.Random) -> GameState:
        raise NotImplementedError()
