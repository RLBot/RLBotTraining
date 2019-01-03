import random
from typing import Any, Mapping, Optional, List

from rlbot.training.training import Grade, Exercise, Result
from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from . import PlayerEventDetector, PlayerEvent


class TrainingTickPacket:
    """A GameTickPacket but with extra preprocessed information."""

    def __init__(self):
        self.game_tick_packet: GameTickPacket = None
        self.player_events: List[PlayerEvent] = []  # events which happened this tick.
        self._player_event_detector = PlayerEventDetector()

    def update(self, game_tick_packet: GameTickPacket):
        self.game_tick_packet = game_tick_packet
        self.player_events = self._player_event_detector.detect_events(game_tick_packet)


class Grader:
    """
    A Grader is a part of an Exercise which judges the game states
    and makes decisions about whether to terminate.
    A Grader can optionally return implementation defined metrics.
    """

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        """ Similar to Exercise.on_tick() but takes a preprocessed data structure. """
        pass  # Continue by default

    def get_metrics(self) -> Mapping[str, Any]:
        return {}  # No metrics by default


class GraderExercise(Exercise):
    """
    The usual base-class for Exercises in this repo.
    Only requires users of this class to implement
        - make_game_state()
        - make_grader()
    """

    def __init__(self, config_path: str):
        assert type(
            self).setup is GraderExercise.setup, 'Must not override setup(). Override make_game_state() instead.'
        self.config_path = config_path
        # The following ones must be re-initialized in setup() for each run of this exercise.
        self.grader: Grader = None
        self.training_tick_packet: TrainingTickPacket = None

    def get_config_path(self) -> str:
        return self.config_path

    def setup(self, rng: random.Random) -> GameState:
        self.grader = self.make_grader()
        self.training_tick_packet = TrainingTickPacket()
        return self.make_game_state(rng)

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Result]:
        assert self.grader, "setup() must be called before on_tick such that self.grader is set."
        self.training_tick_packet.update(game_tick_packet)
        return self.grader.on_tick(self.training_tick_packet)

    def make_game_state(self, rng: random.Random) -> GameState:
        raise NotImplementedError()

    def make_grader(self) -> Grader:
        raise NotImplementedError()
