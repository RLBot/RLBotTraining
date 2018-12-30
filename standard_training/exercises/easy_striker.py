import random
from math import pi
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, StrikerGrader, Grader

class BallInFrontOfGoal(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
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

    def make_grader(self) -> Grader:
        return StrikerGrader()


class FacingAwayFromBallInFrontOfGoal(GraderExercise):
    def __init__(self, config_path, car_start_x, car_start_y=3000):
        super().__init__(config_path)
        self.car_start_x = car_start_x
        self.car_start_y = car_start_y

    def make_game_state(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 100),
                velocity=Vector3(0,0,0),
                angular_velocity=Vector3(0,0,0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(self.car_start_x, self.car_start_y, 0),
                        rotation=Rotator(0, -pi/2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

    def make_grader(self) -> Grader:
        return StrikerGrader()
