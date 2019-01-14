import random
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from ..grading import GraderExercise, GoalieGrader, Grader


# You are placed in the center while the ball rolls towards your goal
class DefendBallRollingTowardsGoal(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(0, 2500, 25)
        ball_pos = Vector3(random.uniform(-200, 200), random.uniform(0, -1500), 100)
        ball_state = BallState(
            Physics(location=ball_pos, velocity=Vector3(0, -1250, 0), angular_velocity=Vector3(0, 0, 0)))
        car_state = CarState(boost_amount=87, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, rotation=Rotator(0, -pi / 2, 0),
                                             velocity=Vector3(0, 0, 0),
                                             angular_velocity=Vector3(0, 0, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

    def make_grader(self) -> Grader:
        return GoalieGrader()


# A test where the ball is put on the line and the player in the middle of the field
class LineSave(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(0, 2500, 25)
        ball_pos = Vector3(0, -5000, 100)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(0, 0, 0), angular_velocity=Vector3(0, 0, 0)))
        car_state = CarState(boost_amount=87, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, rotation=Rotator(0, -pi / 2, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

    def make_grader(self) -> Grader:
        return GoalieGrader()


# A test where your driving at speed towards your own goal with the ball right in front of you
class TryNotToOwnGoal(GraderExercise):

    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(0, 2500, 25)
        ball_pos = Vector3(0, 2000, 100)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(0, -1300, 0)))
        car_state = CarState(boost_amount=0, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, velocity=Vector3(0, -1000, 0),
                                             rotation=Rotator(0, -pi / 2, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state

    def make_grader(self) -> Grader:
        return GoalieGrader()
