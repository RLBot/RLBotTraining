import json
import urllib.request
from pathlib import Path
from typing import Mapping, Any, List

from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.logging_utils import get_logger

from rlbottraining.common_graders.goal_grader import StrikerGrader
from rlbottraining.training_exercise import TrainingExercise, Playlist
from rlbottraining.grading.grader import Grader
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.timeout import PassOnTimeout
from rlbottraining.match_configs import make_empty_match_config
from rlbottraining.paths import ExerciseDataCache
from rlbottraining.rng import SeededRandomNumberGenerator

cache_dir = Path(__file__).absolute().parent / 'download_cache'
logger_id = 'bakkesmod_importer'

# Constants for converting angles
UCONST_Pi = 3.1415926
URotation180 = float(32768)
URotationToRadians = UCONST_Pi / URotation180


class BakkesmodImportedExercise(TrainingExercise):

    def __init__(self, shot_id: str):
        self.shot_json = self._get_shot_json(shot_id)
        super().__init__(
            name=self.shot_json['name'],
            grader=StrikerGrader()
        )

    def _get_shot_json(self, shot_id: str):
        ExerciseDataCache.bakkesmod_shots_dir.mkdir(parents=True, exist_ok=True)
        cache_file_path = ExerciseDataCache.bakkesmod_shots_dir / f'{shot_id}.json'
        if not cache_file_path.exists():
            url = f'https://workshop.bakkesmod.com/static/shots/{shot_id}.json'
            get_logger(logger_id).info(f'Downloading: {url}')
            urllib.request.urlretrieve(url, cache_file_path)
        with open(cache_file_path) as f:
            return json.load(f)

    def make_game_state(self, rng) -> GameState:
        player_json = self.shot_json['start']['player']
        ball_json = self.shot_json['start']['ball']
        return GameState(
            ball=BallState(physics=self._parse_physics(rng, ball_json)),
            cars={
                0: CarState(
                    physics=self._parse_physics(rng, player_json),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=100)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

    def _parse_rotator(self, rng, vec3_json: Mapping[str, str]) -> Rotator:
        return Rotator(
            pitch = URotationToRadians * self._parse_number(rng, vec3_json, 'pitch'),
            yaw   = URotationToRadians * self._parse_number(rng, vec3_json, 'yaw'),
            roll  = URotationToRadians * self._parse_number(rng, vec3_json, 'roll'),
        )


    def _parse_physics(self, rng, physics_json: Mapping[str, Any]) -> Physics:
        return Physics(
                location=self._parse_vec3(rng, physics_json.get('location', {})),
                velocity=self._parse_vec3(rng, physics_json.get('velocity', {})),
                rotation=self._parse_rotator(rng, physics_json.get('rotation', {})),
                angular_velocity=Vector3(0,0,0),
            )
    def _parse_vec3(self, rng, vec3_json: Mapping[str, str]) -> Vector3:
        return Vector3(
            x=self._parse_number(rng, vec3_json, 'x'),
            y=self._parse_number(rng, vec3_json, 'y'),
            z=self._parse_number(rng, vec3_json, 'z'),
        )
    def _parse_number(self, rng, json: Mapping[str, Any], attr_name:str, default_value=0):
        attr = json.get(attr_name, default_value)
        if self._is_number(attr):
            return attr
        assert isinstance(attr, str), f"I don't know how to decdoe this thing which should give a number: {repr(attr)}"
        number_or_tuple = eval(attr, {}, {})  # Note: dangerous
        if self._is_number(number_or_tuple):
            return number_or_tuple
        tup = number_or_tuple
        assert isinstance(tup, tuple), f"I don't know how to decode this thing: {repr(number_or_tuple)}"
        assert len(tup) == 2, f"I only know how to interpret number ranges made of a 2-tuple"
        # TODO: confirm with Bakkes that this is the right way of interpreting the tuple.
        return rng.uniform(tup[0], tup[1])
    def _is_number(self, obj: Any) -> bool:
        return isinstance(obj, float) or isinstance(obj, int)

def exercises_from_bakkesmod_playlist(playlist_id: str) -> List[BakkesmodImportedExercise]:
    ExerciseDataCache.bakkesmod_shots_dir.mkdir(parents=True, exist_ok=True)
    cache_file_path = ExerciseDataCache.bakkesmod_shots_dir / f'{playlist_id}.json'
    if not cache_file_path.exists():
        url = f'https://workshop.bakkesmod.com/maps/playlist/{playlist_id}/list'
        get_logger(logger_id).info(f'Downloading: {url}')
        urllib.request.urlretrieve(url, cache_file_path)
    with open(cache_file_path) as f:
        shots_ids = json.load(f)['shots'].split(',')
    # TODO: parallel download
    return [ BakkesmodImportedExercise(shot_id) for shot_id in shots_ids ]

def make_default_playlist() -> Playlist:
    return exercises_from_bakkesmod_playlist('quJfnUJf22')
