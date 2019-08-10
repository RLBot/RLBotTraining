from pathlib import Path
from dataclasses import dataclass, field
from math import pi
from typing import Callable

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team

from rlbottraining.common_graders.goal_grader import StrikerGrader
from rlbottraining.grading.grader import Grader
from rlbottraining.match_configs import make_empty_match_config
from rlbottraining.paths import BotConfigs
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import Playlist
from rlbottraining.training_exercise import TrainingExercise


striker_team = Team.ORANGE.value

@dataclass
class VersusLineGoalie(TrainingExercise):

    match_config: MatchConfig = field(default_factory=lambda:
        versus_line_goalie_match_config(attacker=BotConfigs.simple_bot))

    grader: StrikerGrader = field(default_factory=lambda: StrikerGrader(timeout_seconds=7, ally_team=striker_team))

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, -1500, 100),
                velocity=Vector3(rng.uniform(-1, 1), 10, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                # Striker
                0: CarState(
                    physics=Physics(
                        location=Vector3(300*rng.n11(), 200*rng.n11(), 15),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    # jumped=False,
                    # double_jumped=False,
                    boost_amount=100),
                # Goalie
                1: CarState(
                    physics=Physics(
                        location=Vector3(0, -5000, 15),
                        rotation=Rotator(0, rng.uniform(-.1, .1), 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    # jumped=True,
                    # double_jumped=True,
                    boost_amount=100),
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

@dataclass
class SecondShot(VersusLineGoalie):

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        vel_mul = rng.uniform(1.5, 2.0)
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, -1500, 100),
                velocity=Vector3(vel_mul * 350 * rng.uniform(-1, 1), vel_mul * -2000, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                # Striker
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 0, 15),
                        rotation=Rotator(0, -pi / 2, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    # jumped=False,
                    # double_jumped=False,
                    boost_amount=100),
                # Goalie
                1: CarState(
                    physics=Physics(
                        location=Vector3(0, -5000, 15),
                        rotation=Rotator(0, rng.uniform(-.1, .1), 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    # jumped=True,
                    # double_jumped=True,
                    boost_amount=100),
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

# TODO: move this into a more general file.
def _mirror_teams(exercise: TrainingExercise, grader_mutator: Callable[[Grader], Grader] = lambda g: g) -> TrainingExercise:
    from rlbot.utils.game_state_util import flip_y_axis
    for player in exercise.match_config.player_configs:
        player.team = 1 - player.team  # 0->1  1->0
    original_make_game_state = exercise.make_game_state
    exercise.make_game_state = lambda rng: flip_y_axis(original_make_game_state(rng))
    exercise.grader = grader_mutator(exercise.grader)
    return exercise


def versus_line_goalie_match_config(attacker: Path, goalie: Path = BotConfigs.line_goalie) -> MatchConfig:
    match_config = make_empty_match_config()
    match_config.player_configs = [
        PlayerConfig.bot_config(attacker, Team.ORANGE),
        PlayerConfig.bot_config(goalie, Team.BLUE),
    ]
    return match_config

def make_default_playlist() -> Playlist:
    return [
        VersusLineGoalie('VersusLineGoalie'),
        SecondShot('SecondShot'),
    ]
