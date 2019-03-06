from dataclasses import dataclass, field
from typing import Iterable

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.game_state_util import GameState
from rlbot.utils.rendering.rendering_manager import RenderingManager

from rlbottraining.grading.grader import Grader
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.match_configs import make_default_match_config

@dataclass
class TrainingExercise:
    name: str
    grader: Grader
    match_config: MatchConfig = field(default_factory=make_default_match_config)

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        raise NotImplementedError()

    def render(self, renderer: RenderingManager):
        """
        This method is called each tick to render exercise debug information.
        This method is called after on_tick().
        It is optional to override this method.
        """
        self.grader.render(renderer)


Playlist = Iterable[TrainingExercise]
