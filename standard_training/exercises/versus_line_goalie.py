import random
from math import pi
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, GoalieGrader, Grader

class VersusLineGoalie(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0*rng.uniform(-840, 840), -1500, 100),
                velocity=Vector3(0, -2000, 0),
                angular_velocity=Vector3(0,0,0))),
            cars={
                # Goalie
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -4000, 0),
                        rotation=Rotator(0, 0, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0),
                # Striker
                1: CarState(
                    physics=Physics(
                        location=Vector3(0, 0, 0),
                        rotation=Rotator(0, pi/2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0),
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

    def make_grader(self) -> Grader:
        return GoalieGrader()
