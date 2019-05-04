from random import Random
from pathlib import Path
from typing import Optional, Callable

from rlbot.matchcomms.client import MatchcommsClient
from rlbot.matchconfig.match_config import MatchConfig
from rlbot.matchconfig.match_config import MatchConfig
from rlbot.training.training import Exercise as RLBotExercise, Grade, Result as _Result
from rlbot.utils.game_state_util import GameState
from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.utils.structures.game_data_struct import GameTickPacket

from rlbottraining.grading.grader import Grader
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.history.exercise_result import ExerciseResult
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import TrainingExercise

class TrainingExerciseAdapter(RLBotExercise):
    """
    This class is designed to translate between the minimal RLBot training API
    and the convenient to use RLBotTraining API.
    It does this by wrapping the TrainingExercise and unwrapping the result.
    """
    def __init__(self, exercise: TrainingExercise):
        # Do some sanity checks that the object looks correct
        # In case the implementer of the exercise made a mistake with ordered arguments.
        # note: prefer to use keyword arguments when using dataclasses
        assert isinstance(exercise, TrainingExercise)
        assert isinstance(exercise.grader, Grader)
        assert isinstance(exercise.name, str)
        assert isinstance(exercise.match_config, MatchConfig)
        self.exercise = exercise
        self.training_tick_packet = TrainingTickPacket()

    def get_name(self) -> str:
        return self.exercise.name

    def get_match_config(self) -> MatchConfig:
        return self.exercise.match_config

    def setup(self, rng: Random) -> GameState:
        return self.exercise.make_game_state(
            SeededRandomNumberGenerator(rng)
        )

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Grade]:
        self.training_tick_packet.update(game_tick_packet)
        return self.exercise.grader.on_tick(self.training_tick_packet)

    def on_briefing(self) -> Optional[Grade]:
        return self.exercise.on_briefing()

    def set_matchcomms_factory(self, matchcomms_factory: Callable[[], MatchcommsClient]):
        self.exercise.matchcomms_factory = matchcomms_factory

    def render(self, renderer: RenderingManager):
        self.exercise.render(renderer)
