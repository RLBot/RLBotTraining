from typing import List

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
