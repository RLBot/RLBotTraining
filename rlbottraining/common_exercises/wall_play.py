from dataclasses import dataclass

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist


@dataclass
class BallRollingTowardsWall(StrikerExercise):
    """A test where the ball is rolling towards the walls"""
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        car_pos = Vector3(0, 250, 25)
        ball_pos = Vector3(500, 0, 100)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(1400, 0, 0)))
        car_state = CarState(boost_amount=100, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, velocity=Vector3(1399, 0, 0),
                                             rotation=Rotator(0, 0, 0)))
        game_state = GameState(ball=ball_state, cars={0: car_state})
        return game_state

def make_default_playlist() -> Playlist:
    return [
        BallRollingTowardsWall('BallRollingTowardsWall'),
    ]
