from pathlib import Path

"""
This file contains a few paths to files (e.g. configs / bots)  which might be
handy to build your own exercises with.
Note: if there are data files which should be included as part of the package,
please also update setup.py
"""

# Do not rely on these private ones for your exercises.
# They allow rlbottraining to be refactored later.
_rlbot_training_dir = Path(__file__).absolute().parent
_example_bot_dir = _rlbot_training_dir / 'example_bots'
_match_config_dir = _rlbot_training_dir / 'rlbot_configs'
_common_exercises_dir = _rlbot_training_dir / 'common_exercises'
_exercise_data_cache_dir = _rlbot_training_dir / 'exercise_data_cache_dir'
_match_config_dir = _rlbot_training_dir / 'match_configs'
# You may rely on the ones below.

class BotConfigs:
    """
    Contains paths to example bots included in this repo.
    """
    brick_bot = _example_bot_dir / 'brick_bot' / 'brick_bot.cfg'
    simple_bot = _example_bot_dir / 'simple_bot' / 'simple_bot.cfg'
    line_goalie = _example_bot_dir / 'line_goalie' / 'line_goalie.cfg'

class HistoryPaths:
    """
    Relative paths within the history directory which contains
    metrics of past training runs.
    """

    # authoritative_data is a directory with files that contain the raw
    # output of training runs.
    # Files in here should be immutable with the caveat of data retention.
    authoritative_data = Path('authoritative_data')

    # # The match_configs directory contains JSON versions of match configs
    # # which are named by a hash of their contents.
    # #
    # match_configs = authoritative_data / 'match_configs'

    reproducable_exercises = authoritative_data / 'reproducable_exercises'
    reproducable_pickle_dir = reproducable_exercises / 'pickle_jar'
    # TODO: reproducable_zip = authoritative_data / 'reproducable_exercises'

    # TODO
    # results = authoritative_data / 'results'

class ExerciseDataCache:
    """
    Contains places where exercise may persist temporary files.
    Directories here may need to be created first when written to.
    """
    bakkesmod_cache_dir = _exercise_data_cache_dir / 'bakkesmod_cache'
    bakkesmod_shots_dir = bakkesmod_cache_dir / 'shots'
    bakkesmod_playlists_dir = bakkesmod_cache_dir / 'playlists'


