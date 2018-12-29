import random
from math import pi
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, StrikerGrader

class BallInFrontOfGoal(GraderExercise):

    def __init__(self, config_path:str):
        super().__init__(config_path, StrikerGrader())

    def setup(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 100),
                velocity=Vector3(0,0,0),
                angular_velocity=Vector3(0,0,0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(rng.uniform(-900, 900), 3000, 0),
                        rotation=Rotator(0, pi/2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )
