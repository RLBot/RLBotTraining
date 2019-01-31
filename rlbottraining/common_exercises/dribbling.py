from dataclasses import dataclass
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator


@dataclass
class Dribbling(StrikerExercise):
    """
    The ball gets placed above you, all you need to do is dribble it in
    """

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        car_pos = Vector3(3500 * rng.n11(), rng.uniform(0, -4000), 25)
        ball_pos = Vector3(car_pos.x, car_pos.y + 500, 500)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(0, 0, 500)))
        car_state = CarState(boost_amount=87, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, velocity=Vector3(0, 0, 0),
                                             rotation=Rotator(0, pi / 2, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

def make_default_playlist():
    return [
        Dribbling('Basic dribble'),
    ]
