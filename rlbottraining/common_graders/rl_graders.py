
"""
This module contains graders which mimic the the behaviour of Rocket League custom training.
"""


from dataclasses import dataclass
from typing import Optional, Mapping, Union

from rlbot.training.training import Pass, Fail, Grade

from rlbottraining.grading.grader import Grader
from rlbottraining.grading.event_detector import PlayerEventType
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.compound_grader import CompoundGrader
from rlbottraining.common_graders.timeout import FailOnTimeout, PassOnTimeout
from rlbottraining.common_graders.goal_grader import PassOnGoalForAllyTeam


class RocketLeagueStrikerGrader(CompoundGrader):
    """
    A Grader which aims to match the striker training.
    """

    def __init__(self, timeout_seconds=4.0, ally_team=0):
        super().__init__([
            PassOnGoalForAllyTeam(ally_team),
            FailOnBallOnGroundAfterTimeout(timeout_seconds),
        ])

class FailOnBallOnGroundAfterTimeout(FailOnTimeout):

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        grade = super().on_tick(tick)
        if grade is None:
            return None
        assert isinstance(grade, FailOnTimeout.FailDueToTimeout)
        ball = tick.game_tick_packet.game_ball.physics
        if ball.location.z < 100 and ball.velocity.z >= 0:
            return grade

