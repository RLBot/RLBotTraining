from pathlib import Path

from rlbottraining.alter_config import alter_config, use_bot
from rlbottraining.exercise_runner import run_exercises, run_module
from rlbottraining.exercises.bakkesmod_import.bakkesmod_importer import exercises_from_bakkesmod_playlist
from rlbottraining.exercises.dribbling import Dribbling
from rlbottraining.exercises.easy_goalie import BallRollingToGoalie
from rlbottraining.exercises.easy_striker import BallInFrontOfGoal, FacingAwayFromBallInFrontOfGoal, RollingTowardsGoalShot
from rlbottraining.exercises.medium_goalie import DefendBallRollingTowardsGoal, LineSave, TryNotToOwnGoal
from rlbottraining.exercises.medium_striker import HookShot
from rlbottraining.exercises.versus_line_goalie import VersusLineGoalie
import rlbottraining.exercises.ball_prediction
from rlbottraining.paths import BotConfigs, MatchConfigs

# TODO: playlists.

current_dir = Path(__file__).absolute().parent
exercise_dir = current_dir / 'rlbottraining' / 'exercises'

def run_easy_exercises():
    config_path = MatchConfigs.single_soccar
    run_exercises({
        'Facing ball': BallInFrontOfGoal(config_path),
        'Facing away from ball 1': FacingAwayFromBallInFrontOfGoal(config_path, 1500.),
        'Facing away from ball 2': FacingAwayFromBallInFrontOfGoal(config_path, -400.),
        'Facing away from ball 3': FacingAwayFromBallInFrontOfGoal(config_path, 0),
        'Facing away from opponents goal': FacingAwayFromBallInFrontOfGoal(config_path, 200., car_start_y=5100),
        'Defend by catching up to ball': DefendBallRollingTowardsGoal(config_path),
        'Rolling Shot': RollingTowardsGoalShot(config_path),
        'Hook Shot': HookShot(config_path),
        'Dribbling': Dribbling(config_path),
        'BallInFrontOfGoal2': BallInFrontOfGoal(config_path),
        'BallRollingToGoalie': BallRollingToGoalie(config_path),
        'BallRollingToGoalie2': BallRollingToGoalie(config_path),
        'Line Save': LineSave(config_path),
        'Try Not To Own Goal': TryNotToOwnGoal(config_path)
    }, infinite=True)


def run_some_bakkesmod_exercises():
    config_path = MatchConfigs.single_soccar
    # You can get a playlist_id by grabbing it out of the URL. e.g.
    # https://workshop.bakkesmod.com/maps/playlist/quJfnUJf22
    playlist_id = 'quJfnUJf22'
    exercises = exercises_from_bakkesmod_playlist(config_path, playlist_id)
    run_exercises(exercises, infinite=True)


def run_versus_line_goalie():
    config_path = MatchConfigs.versus_line_goalie
    run_exercises({
        'BallRollingToGoalie': VersusLineGoalie(config_path),
    }, infinite=True)


def run_with_bot_substitution():
    """
    This example demonstrates how to switch configs for an existing
    config. We begin by using the brick bot config and substituting simple_bot.
    """
    original_config_path = MatchConfigs.single_soccar_brick_bot
    with alter_config(
            original_config_path,
            use_bot(BotConfigs.simple_bot)
    ) as config_path:
        run_exercises({
            'Facing away x=-400 (brick_bot)': FacingAwayFromBallInFrontOfGoal(original_config_path, -400.),
            'Facing away x=1500 (brick_bot)': FacingAwayFromBallInFrontOfGoal(original_config_path, 1500.),
            'Facing away x=-400 (simple_bot)': FacingAwayFromBallInFrontOfGoal(config_path, -400.),
            'Facing away x=1500 (simple_bot)': FacingAwayFromBallInFrontOfGoal(config_path, 1500.),
        }, infinite=True)

def run_ball_prediction_exercises():
    run_module(exercise_dir / 'ball_prediction.py')

if __name__ == '__main__':
    run_easy_exercises()
    # run_some_bakkesmod_exercises()
    # run_versus_line_goalie()
    # run_with_bot_substitution()
    # run_ball_prediction_exercises()
