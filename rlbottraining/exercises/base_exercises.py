from rlbottraining.grading.grader import Grader
from rlbottraining.rng import SeededRandomNumberGenerator

@dataclass
class TrainingExercise:
    match_config: MatchConfig
    grader: Grader = None

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        raise NotImplementedError()

