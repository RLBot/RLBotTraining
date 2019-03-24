from pathlib import Path
from typing import List

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

def make_match_config_with_players(player_configs: List[PlayerConfig]) -> MatchConfig:
    """
    Returns a match config containing the provided players (which can be bots or humans) playing soccar.
    Has some mutators which are usually useful for bot training.
    """
    match_config = make_empty_match_config()
    match_config.player_configs = players
    return match_config


def make_match_config_with_bots(blue_bots: List[Path] = None, orange_bots: List[Path] = None) -> MatchConfig:
    """
    Returns a match config containing the provided bots playing soccar.
    The bot index order will be blue_bots then orange_bots.
    Has some mutators which are usually useful for bot training.
    """
    if blue_bots is None: blue_bots = []
    if orange_bots is None: orange_bots = []
    blue_players   = [ PlayerConfig.bot_config(bot_path, Team.BLUE)   for bot_path in blue_bots]
    orange_players = [ PlayerConfig.bot_config(bot_path, Team.ORANGE) for bot_path in orange_bots]
    return make_match_config_with_players(blue_players + orange_players)

def make_default_match_config() -> MatchConfig:
    """
    Returns a match config containing a single, simple bot playing soccar.
    Has some mutators which are usually useful for bot training.
    """
    return make_match_config_with_bots(blue_bots=[BotConfigs.simple_bot])
