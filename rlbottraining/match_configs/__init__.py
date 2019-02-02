from pathlib import Path

from rlbot.matchconfig.conversions import read_match_config_from_file
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team

from rlbottraining.paths import BotConfigs, _match_config_dir

def make_empty_match_config() -> MatchConfig:
    """
    Returns a parsed rlbot.cfg without any bots.
    You can specify your own bots by doing something similar to
    what get_default_match_config() does.
    Has some mutators which are usually useful for bot training.
    """
    config_path = _match_config_dir / 'empty_soccar.cfg'
    return read_match_config_from_file(config_path)

def make_default_match_config() -> MatchConfig:
    """
    Returns a match config containing a single, simple bot playing soccar.
    Has some mutators which are usually useful for bot training.
    """
    match_config = make_empty_match_config()
    match_config.player_configs = [
        PlayerConfig.bot_config(BotConfigs.simple_bot, Team.BLUE),
    ]
    return match_config
