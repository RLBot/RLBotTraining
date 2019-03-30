from rlbottraining.common_exercises.versus_line_goalie import VersusLineGoalie
from rlbottraining.training_exercise import Playlist
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team


def make_default_playlist() -> Playlist:
    exercises = [
        VersusLineGoalie('VersusLineGoalie'),
        VersusLineGoalie('VersusLineGoalie'),
        VersusLineGoalie('VersusLineGoalie'),
    ]
    for ex in exercises:
        striker = ex.match_config.player_configs[0]
        striker.bot = False
        striker.rlbot_controlled = False
        striker.human_index = 0
        striker.loadout = None
    return exercises
