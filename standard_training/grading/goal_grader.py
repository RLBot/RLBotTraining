from enum import Enum
from collections import namedtuple
from typing import List

from rlbot.training.training import Pass, Fail, Grade
from rlbot.utils.structures.game_data_struct import GameTickPacket, ScoreInfo

from . import Grader, CompoundGrader, FailOnTimeout, PlayerEventType, TrainingTickPacket


class StrikerGrader(CompoundGrader):
    """
    A Grader which acts similarly to the RocketLeague striker training.
    """
    def __init__(self, timeout_seconds=4.0, ally_team=0):
        super().__init__({
            'striker goal': PassOnGoalForAllyTeam(ally_team),
            'timeout': FailOnTimeout(timeout_seconds),
        })

class WrongGoalFail(Fail):
    def __repr__(self):
        return f'{super().__repr__()}: Ball went into the wrong goal.'

# class FailOnGoalForEnemyTeam(Grader):
# TODO

class PassOnGoalForAllyTeam(Grader):
    """
    Terminates the Exercise when any goal is scored.
    Returns a Pass iff the goal was for ally_team,
    otherwise returns a Fail.
    """

    def __init__(self, ally_team: int):
        """
        :param ally_team: number equal to game_datastruct.PlayerInfo.team.
        """
        self.ally_team = ally_team

    def on_tick(self, tick: TrainingTickPacket):
        for event in tick.player_events:
            if event.type == PlayerEventType.GOALS:
                if event.player.team == self.ally_team:
                    return Pass()
                else:
                    return WrongGoalFail()
            elif event.type == PlayerEventType.OWN_GOALS:
                if event.player.team == self.ally_team:
                    return WrongGoalFail()
                else:
                    return Pass()
