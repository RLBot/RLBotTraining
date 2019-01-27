from dataclasses import dataclass, field
from typing import List

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.game_state_util import GameState

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

Playlist = List[TrainingExercise]
