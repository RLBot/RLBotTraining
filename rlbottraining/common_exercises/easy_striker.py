from dataclasses import dataclass, field

import random
from math import pi
from pathlib import Path

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import StrikerExercise

@dataclass
class BallInFrontOfGoal(StrikerExercise):
    def make_game_state(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(rng.uniform(-900, 900), 3000, 0),
                        rotation=Rotator(0, pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


@dataclass
class FacingAwayFromBallInFrontOfGoal(StrikerExercise):

    car_start_x: float = 0
    car_start_y: float = 3000

    def make_game_state(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 4400, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(self.car_start_x, self.car_start_y, 0),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=True,
                    double_jumped=True,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


# The ball is rolling towards goal but you still need to put it in
class RollingTowardsGoalShot(StrikerExercise):
    def make_game_state(self, rng: random.Random) -> GameState:
        car_pos = Vector3(0, -2500, 25)
        ball_pos = Vector3(random.uniform(-1000, 1000), random.uniform(0, 1500), 100)
        ball_state = BallState(Physics(location=ball_pos, velocity=Vector3(0, 550, 0)))
        car_state = CarState(boost_amount=87, jumped=True, double_jumped=True,
                             physics=Physics(location=car_pos, rotation=Rotator(0, pi / 2, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(0, 5120, 25)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state


def make_default_playlist():
    return [
        BallInFrontOfGoal('Facing ball'),
        FacingAwayFromBallInFrontOfGoal('Facing away from ball 1', car_start_x=1500.),
        FacingAwayFromBallInFrontOfGoal('Facing away from ball 2', car_start_x=-400.),
        FacingAwayFromBallInFrontOfGoal('Facing directly away from ball', car_start_x=0),
        # FacingAwayFromBallInFrontOfGoal('Facing away from opponents goal', 200., car_start_y=5100),
        # RollingTowardsGoalShot('Rolling Shot'),
    ]
