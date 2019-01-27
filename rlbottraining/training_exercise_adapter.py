from random import Random
from pathlib import Path
from typing import Optional

from rlbot.training.training import Exercise as RLBotExercise, Grade
from rlbottraining.history.match_config_io import ensure_match_config_on_disk
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import TrainingExercise
from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.rendering.rendering_manager import RenderingManager


class TrainingExerciseAdapter(RLBotExercise):
    """
    This class is designed to translate between the minimal RLBot training API
    and the convenient to use RLBotTraining API.
    """
    def __init__(self, exercise: TrainingExercise, history_dir: Path):
        self.exercise = exercise
        self.history_dir = history_dir
        self.training_tick_packet = TrainingTickPacket()

    def get_config_path(self) -> str:
        return str(ensure_match_config_on_disk(
            self.exercise.match_config,
            self.history_dir
        ))

    def setup(self, rng: Random) -> GameState:
        return self.exercise.make_game_state(
            SeededRandomNumberGenerator(rng)
        )

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Grade]:
        self.training_tick_packet.update(game_tick_packet)
        return self.exercise.grader.on_tick(self.training_tick_packet)

    def render(self, renderer: RenderingManager):
        self.exercise.render(renderer)
