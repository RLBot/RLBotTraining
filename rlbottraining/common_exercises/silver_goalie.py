from dataclasses import dataclass
from math import pi

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import GoalieExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist


@dataclass
class DefendBallRollingTowardsGoal(GoalieExercise):
    """You are placed in the center while the ball rolls towards your goal"""

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(rng.uniform(-200, 200), rng.uniform(0, -1500), 93),
                velocity=Vector3(0, -1300, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 2500, 18),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, -1000, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


@dataclass
class LineSave(GoalieExercise):
    """A test where the ball is put on the line and the player in the middle of the field"""

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, -5000, 93),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 2500, 18),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, -1000, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


@dataclass
class TryNotToOwnGoal(GoalieExercise):
    """A test where your driving at speed towards your own goal with the ball right in front of you"""

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 2000, 93),
                velocity=Vector3(0, -1300, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 2500, 18),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, -1000, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=0),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


def make_default_playlist() -> Playlist:
    return [
        DefendBallRollingTowardsGoal('DefendBallRollingTowardsGoal'),
        LineSave('LineSave'),
        TryNotToOwnGoal('TryNotToOwnGoal'),
    ]
