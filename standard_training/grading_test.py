import random
import unittest

from rlbot.utils.structures.game_data_struct import GameTickPacket, GameInfo
from rlbot.utils.game_state_util import GameState

from grading import Grader, GraderExercise, CompoundGrader, FailOnTimeout, PlayerEventDetector, PlayerEvent, PlayerEventType

"""
This file is a unit test for the grading module which does not require RocketLeague to run.
"""

class GradingTest(unittest.TestCase):

    def test_timeout_ten(self):
        ex = TimeoutExercise('')
        ex.setup(random.Random(7))
        self.assertIsNone(ex.on_tick(packet_with_time(10)))
        self.assertIsNone(ex.on_tick(packet_with_time(13.2)))
        fail_timeout = ex.on_tick(packet_with_time(13.75))
        self.assertIsNotNone(fail_timeout)
        self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)

    def test_timeout_twenty_with_metrics(self):
        ex = TimeoutExercise('')
        ex.setup(random.Random(7))
        self.assertIsNone(ex.on_tick(packet_with_time(20)))
        self.assertIsNone(ex.on_tick(packet_with_time(23.2)))
        fail_timeout = ex.on_tick(packet_with_time(23.75))
        self.assertIsNotNone(fail_timeout)
        self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)

        self.assertDictEqual(ex.grader.get_metrics(), {
            'timeout': {
                'max_duration_seconds': 3.5,
                'initial_seconds_elapsed': 20.0,
                'measured_duration_seconds': 3.75,
            }
        })

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


class TimeoutExercise(GraderExercise):
    def make_game_state(self, rng: random.Random) -> GameState:
        return GameState()

    def make_grader(self) -> Grader:
        return CompoundGrader({
            'timeout': FailOnTimeout(3.5)
        })


def packet_with_time(time: float) -> GameTickPacket:
    return GameTickPacket(game_info=GameInfo(seconds_elapsed=time))


if __name__ == '__main__':
    unittest.main()
