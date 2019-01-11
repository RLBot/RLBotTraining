import random
from pathlib import Path
from typing import Optional

from rlbot.training.training import Exercise, Result
from rlbot.utils.game_state_util import GameState
from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.utils.structures.game_data_struct import GameTickPacket

from . import TrainingTickPacket, Grader


class GraderExercise(Exercise):
    """
    The usual base-class for Exercises in this repo.
    Only requires users of this class to implement
        - make_game_state()
        - make_grader()
    """

    def __init__(self, config_path: Path):
        assert type(self).setup is GraderExercise.setup, (
            'Must not override setup(). Override make_game_state() instead.'
        )
        self.config_path = config_path
        # The following ones must be re-initialized in setup() for each run of this exercise.
        self.grader: Grader = None
        self.training_tick_packet: TrainingTickPacket = None

    def get_config_path(self) -> str:
        return str(self.config_path)

    def setup(self, rng: random.Random) -> GameState:
        self.grader = self.make_grader()
        self.training_tick_packet = TrainingTickPacket()
        return self.make_game_state(rng)

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Result]:
        assert self.grader, "setup() must be called before on_tick such that self.grader is set."
        self.training_tick_packet.update(game_tick_packet)
        return self.grader.on_tick(self.training_tick_packet)

    def render(self, renderer: RenderingManager):
        self.grader.render(renderer)

    def make_game_state(self, rng: random.Random) -> GameState:
        raise NotImplementedError()

    def make_grader(self) -> Grader:
        raise NotImplementedError()
