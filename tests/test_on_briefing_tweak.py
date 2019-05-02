import unittest
from dataclasses import dataclass
from typing import Optional

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.common_base_exercises import GoalieExercise
from rlbottraining.rng import SeededRandomNumberGenerator

@dataclass
class BallRollingToGoalie(GoalieExercise):
    steering_coefficient: float = 5

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, -4000, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, -5800, 0),
                        rotation=Rotator(0, 0, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )


class TweakTest(unittest.TestCase):

    def test_on_briefing_tweak(self):
        print('hi')

if __name__ == '__main__':
    unittest.main()
