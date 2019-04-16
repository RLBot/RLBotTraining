from dataclasses import dataclass, field
from math import pi

from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator

from rlbottraining.common_exercises.rl_custom_training_import.rl_importer import RocketLeagueCustomStrikerTraining
from rlbottraining.common_graders.rl_graders import RocketLeagueStrikerGrader
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist
from rlbottraining.paths import BotConfigs
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team
from rlbottraining.grading.grader import Grader
from rlbottraining.match_configs import make_default_match_config

test_match_config = make_default_match_config()

@dataclass
class SimpleFallFromPerfectStill(RocketLeagueCustomStrikerTraining):

    """Ball starts perfectly still"""

    grader: Grader = RocketLeagueStrikerGrader(timeout_seconds=4, timeout_override=True, ground_override=True)
    test_match_config.player_configs = [PlayerConfig.bot_config(BotConfigs.prop_bot, Team.BLUE), ]
    test_match_config.game_map = "ThrowbackStadium"
    match_config: MatchConfig = test_match_config

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        car_pos = Vector3(5000, 0, 0)
        ball_pos = Vector3(0, 0, 1900)
        ball_vel = Vector3(0, 0, 0)
        ball_ang_vel = Vector3(0, 0, 0)

        ball_state = BallState(Physics(location=ball_pos, velocity=ball_vel, angular_velocity=ball_ang_vel))
        car_state = CarState(boost_amount=100, jumped=False, double_jumped=False,
                             physics=Physics(location=car_pos, rotation=Rotator(0, 0, 0), velocity=Vector3(0, 0, 0),
                                             angular_velocity=Vector3(0, 0, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state


@dataclass
class SimpleFallFromRotatingStill(RocketLeagueCustomStrikerTraining):

    """Ball starts only with angular velocity"""

    grader: Grader = RocketLeagueStrikerGrader(timeout_seconds=5, timeout_override=True, ground_override=True)
    test_match_config.player_configs = [PlayerConfig.bot_config(BotConfigs.prop_bot, Team.BLUE), ]
    test_match_config.game_map = "ThrowbackStadium"
    match_config: MatchConfig = test_match_config

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        car_pos = Vector3(5000, 0, 0)
        ball_pos = Vector3(0, 0, 1900)
        ball_vel = Vector3(15, 0, 0)
        ball_ang_vel = Vector3(1, 1, 1)

        ball_state = BallState(Physics(location=ball_pos, velocity=ball_vel, angular_velocity= ball_ang_vel))
        car_state = CarState(boost_amount=100, jumped=False, double_jumped=False,
                             physics=Physics(location=car_pos, rotation=Rotator(0, 0, 0), velocity=Vector3(0, 0, 0),
                                             angular_velocity=Vector3(0, 0, 0)))
        enemy_car = CarState(physics=Physics(location=Vector3(10000, 10000, 10000)))
        game_state = GameState(ball=ball_state, cars={0: car_state, 1: enemy_car})
        return game_state



def make_default_playlist() -> Playlist:
    return [
        SimpleFallFromPerfectStill('Fall From Perfect Still'),
        #SimpleFallFromRotatingStill('Fall with rotation'),
    ]
