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
_website_source = _rlbot_training_dir / 'history' / 'website'
_website_dev_server = _website_source / 'dev_server.py'
_website_static_source = _website_source / 'static'
_example_rl_custom_training_json = _common_exercises_dir / 'rl_custom_training_import' / '7657-2F43-9B3A-C1F1.json'
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
    Relative paths within the history directory (history_dir) which contains
    metrics of past training runs.
    """

    # authoritative_data is a directory with files that contain the raw
    # output of training runs.
    # Files in here should be immutable with the caveat of data retention.
    authoritative_data = Path('authoritative_data')
    exercise_results = authoritative_data / 'exercise_results'
    additional_website_code = authoritative_data / 'additional_website_code.manual_symlink'  # points to python files or symlinks to python files with contain Aggregators.

    class Website:
        _website_dir = Path('website')
        data_dir = Path('data')

class ExerciseDataCache:
    """
    Contains places where exercise may persist temporary files.
    Directories here may need to be created first when written to.
    """
    bakkesmod_cache_dir = _exercise_data_cache_dir / 'bakkesmod_cache'
    bakkesmod_shots_dir = bakkesmod_cache_dir / 'shots'
    bakkesmod_playlists_dir = bakkesmod_cache_dir / 'playlists'


