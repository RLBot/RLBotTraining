from dataclasses import dataclass
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist


@dataclass
class Dribbling(StrikerExercise):
    """
    The ball gets placed above you, all you need to do is dribble it in
    """

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        car_pos = Vector3(3500 * rng.n11(), rng.uniform(0, -4000), 25)
        ball_pos = Vector3(car_pos.x, car_pos.y + 500, 500)
        return GameState(
            ball=BallState(physics=Physics(
                location=ball_pos,
                velocity=Vector3(0, 0, 500),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=car_pos,
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    boost_amount=87),
                1: CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
            },
        )


def make_default_playlist() -> Playlist:
    return [
        Dribbling('Basic dribble'),
    ]
