from pathlib import Path

from standard_training.exercise_runner import run_exercises
from standard_training.exercises.bakkesmod_import.bakkesmod_importer import exercises_from_bakkesmod_playlist
from standard_training.exercises.ball_prediction import make_ball_prediction_exercises
from standard_training.exercises.easy_goalie import BallRollingToGoalie
from standard_training.exercises.easy_striker import BallInFrontOfGoal, FacingAwayFromBallInFrontOfGoal
from standard_training.exercises.versus_line_goalie import VersusLineGoalie
from standard_training.alter_config import alter_config, use_bot

# TODO: playlists.

current_dir = Path(__file__).absolute().parent
config_dir = current_dir / 'rlbot_configs'
example_bot_dir = current_dir / 'example_bots'

def run_easy_exercises():
    config_path = config_dir / 'single_soccar.cfg'
    run_exercises({
        'Facing ball': BallInFrontOfGoal(config_path),
        'Facing away from ball 1': FacingAwayFromBallInFrontOfGoal(config_path, 1500.),
        'Facing away from ball 2': FacingAwayFromBallInFrontOfGoal(config_path, -400.),
        'Facing away from ball 3': FacingAwayFromBallInFrontOfGoal(config_path, 0),
        'Facing away from opponents goal': FacingAwayFromBallInFrontOfGoal(config_path, 200., car_start_y=5100),

        'BallInFrontOfGoal2': BallInFrontOfGoal(config_path),
        'BallRollingToGoalie': BallRollingToGoalie(config_path),
        'BallRollingToGoalie2': BallRollingToGoalie(config_path),
    }, infinite=True)

def run_some_bakkesmod_exercises():
    config_path = config_dir / 'single_soccar.cfg'
    # You can get a playlist_id by grabbing it out of the URL. e.g.
    # https://workshop.bakkesmod.com/maps/playlist/quJfnUJf22
    playlist_id = 'quJfnUJf22'
    exercises = exercises_from_bakkesmod_playlist(config_path, playlist_id)
    run_exercises(exercises, infinite=True)

def run_versus_line_goalie():
    config_path = config_dir / 'versus_line_goalie.cfg'
    run_exercises({
        'BallRollingToGoalie': VersusLineGoalie(config_path),
    }, infinite=True)

def run_with_bot_substitution():
    """
    This example demonstrates how to switch configs for an existing
    config. We begin by using the brick bot config and substituting simple_bot.
    """
    original_config_path = config_dir / 'single_soccar_brick_bot.cfg'
    with alter_config(
        original_config_path,
        use_bot(example_bot_dir / 'simple_bot' / 'simple_bot.cfg')
    ) as config_path:
        run_exercises({
            'Facing away x=-400 (brick_bot)': FacingAwayFromBallInFrontOfGoal(original_config_path, -400.),
            'Facing away x=1500 (brick_bot)': FacingAwayFromBallInFrontOfGoal(original_config_path, 1500.),
            'Facing away x=-400 (simple_bot)': FacingAwayFromBallInFrontOfGoal(config_path, -400.),
            'Facing away x=1500 (simple_bot)': FacingAwayFromBallInFrontOfGoal(config_path, 1500.),
        }, infinite=True)

def run_with_zero_bots():
    config_path = config_dir / 'single_soccar_brick_bot.cfg'

    run_exercises(make_ball_prediction_exercises(config_path), infinite=True)

if __name__ == '__main__':
    # run_easy_exercises()
    # run_some_bakkesmod_exercises()
    # run_versus_line_goalie()
    # run_with_bot_substitution()
    run_with_zero_bots()
