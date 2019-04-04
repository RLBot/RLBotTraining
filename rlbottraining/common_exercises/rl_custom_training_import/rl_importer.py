"""
Imports rocket league custom training from a format primarily provided by bakkes.
"""

from dataclasses import dataclass, field
import json
import urllib.request
from pathlib import Path
from typing import Dict, Any, List
from functools import reduce
import math

import numpy as np
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.logging_utils import get_logger

from rlbottraining.common_graders.goal_grader import StrikerGrader
from rlbottraining.training_exercise import TrainingExercise, Playlist
from rlbottraining.grading.grader import Grader
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.timeout import PassOnTimeout
from rlbottraining.match_configs import make_empty_match_config
from rlbottraining.paths import _example_rl_custom_training_json
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.common_graders.rl_graders import RocketLeagueStrikerGrader

Json = Dict[str, Any]

@dataclass
class RocketLeagueCustomStrikerTraining(TrainingExercise):
    pass


def import_exercises(json_path: Path) -> List[RocketLeagueCustomStrikerTraining]:
    with open(json_path) as f:
        training_json = json.load(f)
    exercises = []

    training_data = training_json['TrainingData']
    assert training_data['Type'] == 3, 'only striker exercises are implemented so far.'

    map_name_translation = {
        'throwbackstadium_P': 'ThrowbackStadium',
        # TODO: https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/parsing/match_settings_config_parser.py#L40-L78
    }
    game_map = map_name_translation[training_data['MapName']]

    for i, shot in enumerate(training_data['Rounds']):
        timeout_seconds = shot['TimeLimit']

        ball_state = None
        car_state = None
        for obj_str in shot['SerializedArchetypes']:
            obj = json.loads(obj_str)
            if obj.get('IsPC'):
                pass  # Editor camera position.
            elif obj.get('ObjectArchetype', '') == 'Archetypes.Ball.Ball_GameEditor':
                ball_state = parse_ball(obj)
            elif obj.get('ObjectArchetype', '') == 'Archetypes.GameEditor.DynamicSpawnPointMesh':
                car_state = parse_car(obj)
            else:
                raise NotImplementedError(f'I have no idea what this is: {obj_str}')
        assert timeout_seconds is not None
        assert ball_state is not None
        assert car_state is not None
        game_state = GameState(
            ball=ball_state,
            cars={0: car_state},
        )
        def make_make_game_state():
            s = game_state
            return lambda rng: s

        ex = RocketLeagueCustomStrikerTraining(
            name = json_path.name.split('.')[0] + f' [{i}]',
            grader = RocketLeagueStrikerGrader(
                timeout_seconds=timeout_seconds,
            )
        )
        ex.make_game_state = make_make_game_state()
        ex.match_config.game_map = game_map
        exercises.append(ex)

    return exercises

def parse_ball(ball: Json) -> BallState:
    return BallState(physics=Physics(
            location=Vector3(
                x=ball['StartLocationX'],
                y=ball['StartLocationY'],
                z=ball['StartLocationZ'],
            ),
            velocity=parse_ball_vel(ball),
            angular_velocity=Vector3(0,0,0),
        ))
def parse_ball_vel(ball: Json) -> Vector3:
    rot_matrix = to_rotation_matrix(
        URotationToRadians * ball['VelocityStartRotationP'],
        URotationToRadians * ball['VelocityStartRotationY'],
        URotationToRadians * ball['VelocityStartRotationR']
    )
    vec3 = np.dot(rot_matrix, np.array([ball['VelocityStartSpeed'], 0, 0]))
    return Vector3(*vec3)

def parse_car(car: Json) -> CarState:
    return CarState(physics=Physics(
            location=Vector3(
                x=car['LocationX'],
                y=car['LocationY'],
                z=car['LocationZ'],
            ),
            rotation=Rotator(
                URotationToRadians * car['RotationP'],
                URotationToRadians * car['RotationY'],
                URotationToRadians * car['RotationR'],
            ),
            velocity=Vector3(0,0,0),
            angular_velocity=Vector3(0,0,0),
        ),
        boost_amount=100,
        jumped=False,
        double_jumped=False,
    )



UCONST_Pi = 3.1415926
URotation180 = float(32768)
URotationToRadians = UCONST_Pi / URotation180

def to_rotation_matrix(pitch, yaw, roll):
    # Note: Unreal engine coordinate system but angles are in radians.
    y=pitch
    cosy = math.cos(y)
    siny = math.sin(y)
    mat_pitch = np.array(
            [[cosy, 0, -siny],
             [0, 1, 0],
             [siny, 0, cosy]])

    z=yaw
    cosz = math.cos(z)
    sinz = math.sin(z)
    mat_yaw = np.array(
            [[cosz, -sinz, 0],
             [sinz, cosz, 0],
             [0, 0, 1]])

    x=roll
    cosx = math.cos(x)
    sinx = math.sin(x)
    mat_roll = np.array(
            [[1, 0, 0],
             [0, cosx, sinx],
             [0, -sinx, cosx]])

    return reduce(np.dot, [mat_yaw, mat_pitch, mat_roll])

def make_default_playlist():
    exercises = import_exercises(_example_rl_custom_training_json)
    # exercises = exercises[0:3]
    return exercises

if __name__ == '__main__':
    exs = make_default_playlist()
    print(exs[0])

