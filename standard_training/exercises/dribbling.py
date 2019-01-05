import random
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, StrikerGrader, Grader


class Dribbling(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(random.uniform(-3500, 3500), random.uniform(0, -4000), 25)
        ball_pos = Vector3(car_pos.x, car_pos.y + 500, 500)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(0, 0, 500)))
        car_state = CarState(boost_amount=87, physics=Physics(location=car_pos, velocity=Vector3(0, 0, 0),
                                                              rotation=Rotator(0, pi / 2, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

    def make_grader(self) -> Grader:
        return StrikerGrader()
