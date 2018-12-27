import unittest

from rlbot.training.training import Exercise, Pass, Fail, Grade
from rlbot.utils.structures.game_data_struct import GameTickPacket, GameInfo
from grading import Grader, CompoundGrader, FailOnTimeout

class GradingTest(unittest.TestCase):

    def test_ten(self):
        ex = TimeoutExercise()
        self.assertIsNone(ex.on_tick(packet_with_time(10)))
        self.assertIsNone(ex.on_tick(packet_with_time(13.2)))
        fail_timeout = ex.on_tick(packet_with_time(13.75))
        self.assertIsNotNone(fail_timeout)
        self.assertIsInstance(fail_timeout, FailOnTimeout.FailDueToTimeout)

    def test_twenty_with_metrics(self):
        ex = TimeoutExercise()
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

class TimeoutExercise(Exercise):
    def __init__(self):
        self.grader = CompoundGrader({
            'timeout': FailOnTimeout(3.5)
        })

    def on_tick(self, game_tick_packet):
        return self.grader.on_tick(game_tick_packet)

def packet_with_time(time:float) -> GameTickPacket:
    return GameTickPacket(game_info=GameInfo(seconds_elapsed=time))



if __name__ == '__main__':
    unittest.main()
