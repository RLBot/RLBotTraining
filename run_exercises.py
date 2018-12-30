from os.path import join, dirname

from standard_training.exercises.easy_striker import BallInFrontOfGoal
from standard_training.exercise_runner import run_exercises

def run_easy_exercises():
    config_path = join(dirname(__file__), 'rlbot_configs', 'single_soccar.cfg')
    run_exercises({
        'BallInFrontOfGoal': BallInFrontOfGoal(config_path),
        'BallInFrontOfGoal2': BallInFrontOfGoal(config_path),
    }, infinite=True)

if __name__ == '__main__':
    run_easy_exercises()
