from typing import Dict, Optional
import random
from pathlib import Path
from math import tau

from rlbot.training.training import Pass, Fail, Grade
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.rendering.rendering_manager import RenderingManager

from ..grading import GraderExercise, Grader, TrainingTickPacket, Grader, PassOnTimeout

"""
This module contains exercises which does not test any bots at all!
But it does test ball prediction.
"""

class BallPredictionExercise(GraderExercise):

    def make_grader(self) -> Grader:
        return FailOnInconsistentBallPrediction()

def make_exercises() -> Dict[str, GraderExercise]:
    current_dir = Path(__file__).absolute().parent
    config_dir = current_dir.parent.parent / 'rlbot_configs'
    config_path = config_dir / 'single_soccar_brick_bot.cfg'
    return {
        # 'PredictBallInAir': PredictBallInAir(config_path),
        'SlidingIntoRolling': SlidingIntoRolling(config_path),
    }

cars_in_goal = {
    0: CarState(
        physics=Physics(
            location=Vector3(0, -5700, 30),
            rotation=Rotator(0, 0, 0),
            velocity=Vector3(0, 0, 0),
            angular_velocity=Vector3(0, 0, 0)),
        jumped=True,
        double_jumped=True,
        boost_amount=100),
}

class PredictBallInAir(BallPredictionExercise):
    def make_game_state(self, rng: random.Random) -> GameState:
        def n11():
            """A Shorthand to get a random value between negative 1 and 1. """
            nonlocal rng
            return rng.uniform(-1, 1)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(200*n11(), 1000*n11(), 1000),
                velocity=Vector3(100*n11(), 500*n11(), 700),
                angular_velocity=Vector3(0, 0, 0))),
            cars=cars_in_goal,
        )

class SlidingIntoRolling(BallPredictionExercise):
    def make_game_state(self, rng: random.Random) -> GameState:
        speed = rng.uniform(10, 1800)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4000, 100),
                velocity=Vector3(rng.uniform(-1, 1) * speed, -2*speed, 0),
                angular_velocity=Vector3(0,0,0))),
            cars=cars_in_goal
        )


class FailOnInconsistentBallPrediction(Grader):
    def __init__(self, max_duration_seconds=2.0):
        super().__init__()
        self.pass_on_timeout = PassOnTimeout(max_duration_seconds)

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        # TODO: Fail on inconsistency
        return self.pass_on_timeout.on_tick(tick)

    def render(self, renderer: RenderingManager):
        renderer.begin_rendering('block intercept')
        location = (0,0,100)
        renderer.draw_rect_3d(location, 10, 10, True, renderer.blue(), True)
        renderer.end_rendering()
