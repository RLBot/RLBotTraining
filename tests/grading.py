import random
import unittest
from dataclasses import dataclass, field
import tempfile
from pathlib import Path

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.training.training import Exercise as RLBotExercise
from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket, GameInfo
from rlbot.training.training import Fail

from rlbottraining.common_graders.compound_grader import CompoundGrader
from rlbottraining.common_graders.timeout import FailOnTimeout
from rlbottraining.grading.event_detector import PlayerEvent, PlayerEventDetector, PlayerEventType
from rlbottraining.grading.grader import Grader
from rlbottraining.training_exercise import TrainingExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise_adapter import TrainingExerciseAdapter

"""
This file is a unit test for the grading module which does not require RocketLeague to run.
"""

test_match_config = MatchConfig()

class GradingTest(unittest.TestCase):

    def test_timeout_ten(self):
        ex: RLBotExercise = TrainingExerciseAdapter(
            TimeoutExercise(name='time to test'),
        )
        self.assertIsInstance(ex.setup(random.Random(7)), GameState)
        self.assertIsNone(ex.on_tick(packet_with_time(10)))
        self.assertIsNone(ex.on_tick(packet_with_time(13.2)))
        fail_timeout = ex.on_tick(packet_with_time(13.75))
        self.assertIsNotNone(fail_timeout)
        self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)
        self.assertIsInstance(fail_timeout, Fail)

        match_config = ex.get_match_config()
        self.assertIs(match_config, test_match_config)

    def test_timeout_twenty_with_metrics(self):
        ex: RLBotExercise = TrainingExerciseAdapter(
            TimeoutExercise(name='time to test'),
        )
        self.assertIsInstance(ex.setup(random.Random(8)), GameState)
        self.assertIsNone(ex.on_tick(packet_with_time(20)))
        self.assertIsNone(ex.on_tick(packet_with_time(23.2)))
        fail_timeout = ex.on_tick(packet_with_time(23.75))
        self.assertIsNotNone(fail_timeout)
        self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)
        self.assertIsInstance(fail_timeout, Fail)


    def test_player_events(self):
        detector = PlayerEventDetector()
        gtp = GameTickPacket()
        gtp.game_info.seconds_elapsed = 14.
        gtp.num_cars = 2
        gtp.game_cars[1].score_info.goals = 3
        self.assertListEqual(detector.detect_events(gtp), [])
        self.assertListEqual(detector.detect_events(gtp), [])
        gtp = GameTickPacket()
        gtp.game_info.seconds_elapsed = 15.
        gtp.num_cars = 2
        gtp.game_cars[1].score_info.goals = 5
        self.assertListEqual(detector.detect_events(gtp), [PlayerEvent(
            type=PlayerEventType.GOALS,
            player=gtp.game_cars[1],
            seconds_elapsed=15.,
        )])
        self.assertListEqual(detector.detect_events(gtp), [])

@dataclass
class TimeoutExercise(TrainingExercise):
    grader: Grader = field(
        default_factory=lambda: CompoundGrader([FailOnTimeout(3.5)])
    )
    match_config: MatchConfig = test_match_config
    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState()



def packet_with_time(time: float) -> GameTickPacket:
    return GameTickPacket(game_info=GameInfo(seconds_elapsed=time))


if __name__ == '__main__':
    unittest.main()
