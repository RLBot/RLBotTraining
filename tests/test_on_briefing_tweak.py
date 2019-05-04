import unittest
from dataclasses import dataclass, field
from typing import Optional

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.matchcomms.common_uses.set_attributes_message import make_set_attributes_message
from rlbot.matchcomms.common_uses.reply import send_and_wait_for_replies
from rlbot.training.training import Grade, Pass, Fail
from rlbot.matchconfig.match_config import MatchConfig

from rlbottraining.paths import BotConfigs
from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.exercise_runner import run_playlist
from rlbottraining.match_configs import make_match_config_with_bots

@dataclass
class TurnAndDriveToBall(StrikerExercise):
    steering_coefficient: float = 5

    match_config: MatchConfig = field(default_factory=lambda:
        make_match_config_with_bots(blue_bots=[BotConfigs.tweaked_bot]))


    def on_briefing(self) -> Optional[Grade]:
        import time
        time.sleep(0.1)  # TODO: retry in send_and_wait_for_replies
        _ = send_and_wait_for_replies(self.get_matchcomms(), [
            make_set_attributes_message(0, {'steering_coefficient': self.steering_coefficient}),
        ])

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 5100, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(-200, 3000, 0),
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
        # We want to assert that this constant is better than other constants.
        ex = TurnAndDriveToBall(name='Turn to ball', steering_coefficient=4)
        result = list(run_playlist([ex]))[0]
        print('result', result)

def make_default_playlist():
    return [TurnAndDriveToBall(name='Turn to ball', steering_coefficient=1.40)]

if __name__ == '__main__':
    unittest.main()
