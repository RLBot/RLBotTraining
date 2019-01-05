import os
from contextlib import contextmanager
from typing import List, Callable
from pathlib import Path
from tempfile import NamedTemporaryFile

from rlbot.parsing.rlbot_config_parser import create_bot_config_layout, parse_configurations, EXTENSION_PATH_KEY
from rlbot.parsing.custom_config import ConfigObject, ConfigHeader
from rlbot.parsing.agent_config_parser import PARTICIPANT_CONFIGURATION_HEADER, PARTICIPANT_CONFIG_KEY, PARTICIPANT_LOADOUT_CONFIG_KEY
from rlbot.parsing.match_settings_config_parser import get_num_players
# A function which takes a config and makes changes to it.
ConfigMutator = Callable[[ConfigObject], None]

@contextmanager
def alter_config(config_path: Path, mutator: ConfigMutator):
    """
    Creates a temporary copy of the RLBot match config file
    with changes applied by the mutator.
    Useful if there is a shared exercise and you want to use your own bot.
    """
    config_path = Path(config_path).absolute()
    config = create_bot_config_layout()
    config.init_indices(10)
    config.parse_file(config_path)
    mutator(config)

    with NamedTemporaryFile(
        mode='w',
        prefix=f'{config_path.name}_altered_',
        suffix='.cfg',
        dir=config_path.parent,
        delete=False
    ) as f:
        try:
            f.write(str(config))
            f.close()
            yield Path(f.name)
        finally:
            os.remove(f.name)

def use_bot(bot_cfg: Path, bot_loadout_cfg: Path=None, bot_indecies: List[int]=None) -> ConfigMutator:
    """
    Replaces bots in the config with the bot.
    :param bot_cfg: The path to the bot config file. If it is a relative path,
    it interpreted relative to Python's `Path().cwd()`.
    :param bots_looks_cfg: Similar to bot_cfg but specifies the cosmetics.
    :param bot_indecies: A list specifying which bots in the config to modify.
    If None, all bots in the config will be set to the given bot.
    """
    bot_cfg = bot_cfg.absolute()
    def use_bot_mutator(config: ConfigObject):
        nonlocal bot_cfg
        nonlocal bot_indecies
        nonlocal bot_loadout_cfg
        if bot_indecies is None:
            bot_indecies = range(get_num_players(config))
        for i in bot_indecies:
            test = config.set_value(
                PARTICIPANT_CONFIGURATION_HEADER,
                PARTICIPANT_CONFIG_KEY,
                bot_cfg,
                index=i
            )
            if bot_loadout_cfg is not None:
                config.set_value(
                    PARTICIPANT_CONFIGURATION_HEADER,
                    PARTICIPANT_LOADOUT_CONFIG_KEY,
                    bot_cfg,
                    index=i
                )
    return use_bot_mutator

def compose_mutators(mutators: List[ConfigMutator]) -> ConfigMutator:
    """
    Applies the given mutators in order.
    May be useful if you want to substitute multiple different bots.
    """
    def composed_mutator(cfg: ConfigObject):
        nonlocal mutators
        for mutator in mutators:
            mutator(cfg)
    return composed_mutator

