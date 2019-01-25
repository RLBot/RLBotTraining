import random

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, StrikerGrader, Grader


# A test where the ball is rolling towards the walls
class BallRollingTowardsWall(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(0, 250, 25)
        ball_pos = Vector3(500, 0, 100)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(1400, 0, 0)))
        car_state = CarState(boost_amount=100, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, velocity=Vector3(1399, 0, 0),
                                             rotation=Rotator(0, 0, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

    def make_grader(self) -> Grader:
        return StrikerGrader()
