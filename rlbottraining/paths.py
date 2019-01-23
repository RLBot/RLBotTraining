from pathlib import Path

"""
This file contains a few paths to configs / bots which might be handy to build
your own exercises,
"""

# Do not rely on these private ones - they allow rlbottraining to be refactored later.
_rlbot_training_dir = Path(__file__).absolute().parent
_example_bot_dir = _rlbot_training_dir / 'example_bots'
_match_config_dir = _rlbot_training_dir / 'rlbot_configs'
# You may rely on the ones below.

class BotConfigs:
    """
    Contains paths to example bots included in this repo.
    """
    brick_bot = _example_bot_dir / 'brick_bot' / 'brick_bot.cfg'
    simple_bot = _example_bot_dir / 'simple_bot' / 'simple_bot.cfg'
    line_goalie = _example_bot_dir / 'line_goalie' / 'line_goalie.cfg'

class MatchConfigs:
    """
    Contains paths to standard configs which would be applicable to many types of exercises.
    """
    single_soccar = _match_config_dir / 'single_soccar.cfg'
    single_soccar_brick_bot = _match_config_dir / 'single_soccar_brick_bot.cfg'
    versus_line_goalie = _match_config_dir / 'versus_line_goalie.cfg'
