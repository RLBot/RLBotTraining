from dataclasses import dataclass, field
from typing import Iterable, Optional, Callable

from rlbot.matchcomms.client import MatchcommsClient
from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.game_state_util import GameState
from rlbot.utils.rendering.rendering_manager import RenderingManager

from rlbottraining.grading.grader import Grader, Grade
from rlbottraining.history.metric import Metric
from rlbottraining.match_configs import make_default_match_config
from rlbottraining.rng import SeededRandomNumberGenerator

@dataclass
class TrainingExercise(Metric):
    name: str
    grader: Grader
    match_config: MatchConfig = field(default_factory=make_default_match_config)

    # MatchcommsClient connected to the current match
    _matchcomms: Optional[MatchcommsClient] = None
    matchcomms_factory: Callable[[], MatchcommsClient] = None  # Initialized externally.
    def get_matchcomms(self) -> MatchcommsClient:
        if not self._matchcomms:
            assert self.matchcomms_factory
            self._matchcomms = self.matchcomms_factory()
        return self._matchcomms

    def on_briefing(self) -> Optional[Grade]:
        """
        This method is called before state-setting such that bots can be "briefed" on the upcoming exercise.
        The "briefing" is usually for using matchcomms to convey objectives and parameters.
        A grade can be returned in case bot responded sufficient to pass or fail the exercise
        before any on_tick() grading happens.
        """
        pass

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        raise NotImplementedError()

    def render(self, renderer: RenderingManager):
        """
        This method is called each tick to render exercise debug information.
        This method is called after on_tick().
        It is optional to override this method.
        """
        self.grader.render(renderer)


Playlist = Iterable[TrainingExercise]
