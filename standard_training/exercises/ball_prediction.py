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

def make_ball_prediction_exercises(config_path: Path) -> Dict[str, BallPredictionExercise]:
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
                location=Vector3(0, 0, 1000),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={},
            boosts={i: BoostState(0) for i in range(34)},
        )


class FailOnInconsistentBallPrediction(Grader):
    def __init__(self, max_duration_seconds=2.0):
        super().__init__()
        self.pass_on_timeout = PassOnTimeout(max_duration_seconds)

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        return self.pass_on_timeout.on_tick(tick)
