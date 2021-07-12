import math

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator
from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist


# The ball is bouncings towards you
class BouncingShotTowardsAgent(StrikerExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 2500, 93),
                velocity=Vector3(0, -250, 700),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 0, 18),
                        velocity=Vector3(0, 0, 0),
                        rotation=Rotator(0, math.pi / 2, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
        )


# The ball is bouncings away from you
class BouncingShotAwayFromAgent(StrikerExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 1500, 93),
                velocity=Vector3(0, 650, 750),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -1000, 18),
                        velocity=Vector3(0, 0, 0),
                        rotation=Rotator(0, math.pi / 2, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
        )


# You need to turn or use a air roll shot
class BouncingShotAngled(StrikerExercise):
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 0, 750),
                velocity=Vector3(0, 0, 1),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(-1000, -1500, 18),
                        velocity=Vector3(0, 0, 0),
                        rotation=Rotator(0, math.pi / 8, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
        )


def make_default_playlist() -> Playlist:
    return [
        BouncingShotTowardsAgent('Bouncing towards'),
        BouncingShotAwayFromAgent('Bouncing away'),
        BouncingShotAngled('Angled bounce shot')
    ]
