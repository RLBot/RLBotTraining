from os.path import join, dirname

from standard_training.exercise_runner import run_exercises
from standard_training.exercises.bakkesmod_import.bakkesmod_importer import exercises_from_bakkesmod_playlist
from standard_training.exercises.easy_goalie import BallRollingToGoalie
from standard_training.exercises.easy_striker import BallInFrontOfGoal, FacingAwayFromBallInFrontOfGoal
from standard_training.exercises.defending import DefendingShot


# TODO: playlists.

def run_easy_exercises():
    config_path = join(dirname(__file__), 'rlbot_configs', 'single_soccar.cfg')
    run_exercises({
        'Facing ball': BallInFrontOfGoal(config_path),
        'Facing away from ball 1': FacingAwayFromBallInFrontOfGoal(config_path, 1500.),
        'Facing away from ball 2': FacingAwayFromBallInFrontOfGoal(config_path, -400.),
        'Facing away from ball 3': FacingAwayFromBallInFrontOfGoal(config_path, 0),
        'Facing away from opponents goal': FacingAwayFromBallInFrontOfGoal(config_path, 200., car_start_y=5100),
        'Defending': DefendingShot(config_path),
        'BallInFrontOfGoal2': BallInFrontOfGoal(config_path),
        'BallRollingToGoalie': BallRollingToGoalie(config_path),
        'BallRollingToGoalie2': BallRollingToGoalie(config_path),
    }, infinite=True)


def run_some_bakkesmod_exercises():
    config_path = join(dirname(__file__), 'rlbot_configs', 'single_soccar.cfg')
    # You can get a playlist_id by grabbing it out of the URL. e.g.
    # https://workshop.bakkesmod.com/maps/playlist/quJfnUJf22
    playlist_id = 'quJfnUJf22'
    exercises = exercises_from_bakkesmod_playlist(config_path, playlist_id)

if __name__ == '__main__':
    run_easy_exercises()
    # run_some_bakkesmod_exercises()
