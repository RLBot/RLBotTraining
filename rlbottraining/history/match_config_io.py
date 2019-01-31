import json
from pathlib import Path
import hashlib

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.matchconfig.conversions import read_match_config_from_file, ConfigJsonEncoder, as_match_config

from rlbottraining.paths import HistoryPaths

def ensure_match_config_on_disk(match_config: MatchConfig, history_dir: Path) -> Path:
    """
    Writes the match_config to disk within the history_dir.
    Will try to write to a file with the same contents.
    """
    json_str = json.dumps(match_config, cls=ConfigJsonEncoder, sort_keys=True)
    json_bytes = bytes(json_str, 'utf8')
    hexdigest = hashlib.sha256(json_bytes).hexdigest()
    match_config_dir = history_dir / HistoryPaths.reproducable_pickle_dir
    match_config_dir.mkdir(parents=True, exist_ok=True)
    hash_named_file = match_config_dir / f'{hexdigest}.json'
    if hash_named_file.exists():
        with open(hash_named_file, 'rb') as f:
            assert f.read() == json_bytes, f"OMG, found a sha256 hash collision on {hash_named_file}"
    else:
        with open(hash_named_file, 'wb') as f:
            f.write(json_bytes)
    return hash_named_file

def parse_match_config(hash_named_file: Path) -> MatchConfig:
    with open(hash_named_file) as f:
        return json.load(f, object_hook=as_match_config)
