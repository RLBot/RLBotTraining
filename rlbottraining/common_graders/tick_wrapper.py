from copy import deepcopy
from typing import Optional, Union
from dataclasses import dataclass

from rlbot.training.training import Pass, Fail, Grade
from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.utils.structures.game_data_struct import GameTickPacket

from rlbottraining.grading.grader import Grader, TrainingTickPacket
from rlbottraining.history.metric import Metric


class GameTickPacketWrapperGrader(Grader):
    """
    Always returns a Grade that has the first and last tick,
    regardless of the actual grade returned by the inner_grader.
    """

    @dataclass
    class WrappedPass(Pass):
        first_tick: GameTickPacket
        last_tick: GameTickPacket
        inner_grade: Pass
        def __str__(self):
            return f'{self.inner_grade} (wrapped with tick)'

    @dataclass
    class WrappedFail(Fail):
        first_tick: GameTickPacket
        last_tick: GameTickPacket
        inner_grade: Fail
        def __str__(self):
            return f'{self.inner_grade} (wrapped with tick)'

    def __init__(self, inner_grader: Grader):
        self.first_tick: Optional[GameTickPacket] = None
        self.inner_grader = inner_grader

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Union[WrappedPass, WrappedFail]]:
        if self.first_tick is None:
            self.first_tick = deepcopy(tick.game_tick_packet)

        inner_grade = self.inner_grader.on_tick(tick)
        if inner_grade is None:
            return None
        if isinstance(inner_grade, Pass): return self.WrappedPass(first_tick=self.first_tick, last_tick=deepcopy(tick.game_tick_packet), inner_grade=inner_grade)
        if isinstance(inner_grade, Fail): return self.WrappedFail(first_tick=self.first_tick, last_tick=deepcopy(tick.game_tick_packet), inner_grade=inner_grade)
        assert False, f'Expected {self.inner_grader.on_tick} to return either None or a Pass/Fail. {inner_grade} was returned'

    def render(self, renderer: RenderingManager):
        self.inner_grader.render(renderer)

