import copy
from typing import List, Optional

from rlbot.training.training import Exercise, Pass, Fail, Grade
from rlbot.utils.structures.game_data_struct import GameTickPacket, Touch

from . import Grader


class RecordBallTouches(Grader):

    def __init__(self):
        self.touches: List[Touch] = []
        self.initial_seconds_elapsed: float = None

    def on_tick(self, game_tick_packet: GameTickPacket) -> Optional[Grade]:
        if self.initial_seconds_elapsed is None:
            self.initial_seconds_elapsed = game_tick_packet.game_info.seconds_elapsed

        # Record the touch only if it is new and happened while we were grading.
        latest_touch = game_tick_packet.game_ball.latest_touch
        if latest_touch.time_seconds < self.initial_seconds_elapsed:
            return
        if self.touches and latest_touch.time_seconds == self.touches[-1]:
            return
        self.touches.append(copy.deepcopy(latest_touch))
        # TODO: maybe impose a limit on the number of touches recorded? To prevent OOM and unnecessarily big datasets.
        return # This grader never terminates the exercise.

    def get_metrics(self) -> Mapping[str, Any]:
        return {
            'ball_touches': self.touches,
        }
