from typing import Dict, Optional
import random
from pathlib import Path

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.training.training import Pass, Fail, Grade

from ..grading import GraderExercise, Grader, TrainingTickPacket, Grader, PassOnTimeout

"""
This module contains exercises which does not test any bots at all!
But it does test ball prediction.
"""

class BallPredictionExercise(GraderExercise):

    def make_grader(self) -> Grader:
        return FailOnInconsistentBallPrediction()

def get_exercises() -> Dict[str, GraderExercise]:
    current_dir = Path(__file__).absolute().parent
    config_dir = current_dir.parent.parent / 'rlbot_configs'
    config_path = config_dir / 'single_soccar_brick_bot.cfg'
    return {
        'PredictBallInAir': PredictBallInAir(config_path),
    }

class PredictBallInAir(BallPredictionExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        def n11():
            """A Shorthand to get a random value between negative 1 and 1. """
            nonlocal rng
            return rng.uniform(-1, 1)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 1000*n11(), 1000),
                velocity=Vector3(0, 0, 700),
                angular_velocity=Vector3(0, 0, 0))),
            cars={},
            boosts={i: BoostState(0) for i in range(34)},
        )


class FailOnInconsistentBallPrediction(Grader):
    def __init__(self, max_duration_seconds=2.0):
        super().__init__()
        self.pass_on_timeout = PassOnTimeout(max_duration_seconds)

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        # TODO: Fail on inconsistency
        return self.pass_on_timeout.on_tick(tick)
