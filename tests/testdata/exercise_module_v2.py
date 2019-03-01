from rlbottraining.training_exercise import Playlist
from rlbottraining.common_exercises.bronze_striker import FacingAwayFromBallInFrontOfGoal

def make_default_playlist() -> Playlist:
    return [
        FacingAwayFromBallInFrontOfGoal('Facing away from ball [0]', car_start_x=5.),
        FacingAwayFromBallInFrontOfGoal('Facing away from ball [1]', car_start_x=6.),  # This should be run due to reloading
    ]
