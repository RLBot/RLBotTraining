from rlbottraining.training_exercise import Playlist
from rlbottraining.common_exercises.bronze_striker import FacingAwayFromBallInFrontOfGoal

def make_default_playlist() -> Playlist:
    return [
        FacingAwayFromBallInFrontOfGoal('Facing away from ball [0]', car_start_x=3.),
        FacingAwayFromBallInFrontOfGoal('Facing away from ball [1]', car_start_x=4.),  # This should not be run as we should reload before reaching this.
    ]
