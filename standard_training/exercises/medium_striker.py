import random
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, StrikerGrader, Grader


class HookShot(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(2000, 500, 25)
        ball_pos = Vector3(2000, 1000, 100)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(0, 1000, 0)))
        car_state = CarState(boost_amount=0, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, velocity=Vector3(0, 1000, 0),
                                             rotation=Rotator(0, pi / 2, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

    def make_grader(self) -> Grader:
        return StrikerGrader()
