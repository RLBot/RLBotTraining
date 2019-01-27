from os import makedirs
import json
from pathlib import Path

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.matchconfig.conversions import read_match_config_from_file, ConfigJsonEncoder, as_match_config

from rlbottraining.paths import HistoryPaths

def ensure_match_config_on_disk(match_config: MatchConfig, history_dir: Path) -> Path:
    """
    Writes the match_config to disk within the history_dir.
    The file may already exist.
    """
    json_str = json.dumps(match_config, cls=ConfigJsonEncoder, sort_keys=True)
    hexdigest = hashlib.sha256(json_str).hexdigest()
    match_config_dir = history_dir / HistoryPaths.match_configs
    makedirs(match_config_dir, exist_ok=True)
    hash_named_file = match_config_dir / f'{hexdigest}.json'
    with open(hash_named_file, 'w') as f:
        f.write(json_str)
    return hash_named_file

def parse_match_config(hash_named_file: Path) -> MatchConfig:
    with open(hash_named_file) as f:
        return json.load(f, object_hook=as_match_config)
