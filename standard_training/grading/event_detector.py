import ctypes
from enum import Enum
from collections import namedtuple
from typing import List

from rlbot.utils.structures.game_data_struct import GameTickPacket, ScoreInfo


PlayerEvent = namedtuple('Event', 'type player seconds_elapsed')
class PlayerEventType(Enum):
    SCORE = 1
    GOALS = 2
    OWN_GOALS = 3
    ASSISTS = 4
    SAVES = 5
    SHOTS = 6
    DEMOLITIONS = 7


class PlayerEventDetector():
    """
    Makes a queue of dicrete things which change between on_tick() calls.
    """
    def __init__(self):
        self.prev_tick_packet = None

    def detect_events(self, game_tick_packet) -> List[PlayerEvent]:
        """
        Detects any PlayerEvents which happened since the last call.
        """
        events = []
        if not self.prev_tick_packet:
            self.prev_tick_packet = GameTickPacket()
        else: # compate to prev_tick_packet
            seconds_elapsed = game_tick_packet.game_info.seconds_elapsed
            for i, player, prev_player in zip(
                range(game_tick_packet.num_cars),
                game_tick_packet.game_cars,
                self.prev_tick_packet.game_cars
            ):
                score = player.score_info
                prev_score = prev_player.score_info
                if score.score != prev_score.score: events.append(PlayerEvent(PlayerEventType.SCORE, player, seconds_elapsed))
                if score.goals != prev_score.goals: events.append(PlayerEvent(PlayerEventType.GOALS, player, seconds_elapsed))
                if score.own_goals != prev_score.own_goals: events.append(PlayerEvent(PlayerEventType.OWN_GOALS, player, seconds_elapsed))
                if score.assists != prev_score.assists: events.append(PlayerEvent(PlayerEventType.ASSISTS, player, seconds_elapsed))
                if score.saves != prev_score.saves: events.append(PlayerEvent(PlayerEventType.SAVES, player, seconds_elapsed))
                if score.shots != prev_score.shots: events.append(PlayerEvent(PlayerEventType.SHOTS, player, seconds_elapsed))
                if score.demolitions != prev_score.demolitions: events.append(PlayerEvent(PlayerEventType.DEMOLITIONS, player, seconds_elapsed))

        ctypes.pointer(self.prev_tick_packet)[0] = game_tick_packet  # memcpy

        return events
