import unittest
import json

from rlbottraining.grading.grader import Grader
from rlbottraining.metrics.metric import Metric
from rlbottraining.metrics.metric_json_encoder import MetricJsonEncoder

from .utils.example_metrics import ExampleMetric, ExampleMetric2

class MetricsTest(unittest.TestCase):

    def test_dataclass(self):
        """
        Just make sure we understand Data Classes properly.
        """
        red_dude = ExampleMetric2(5, (3,0,4))
        self.assertEqual(repr(red_dude), 'ExampleMetric2(speed=5, momentum=(3, 0, 4), violence=True)')
        self.assertIsInstance(red_dude, Metric)
        red_dude2 = ExampleMetric2(5, (3,0,4), True)
        self.assertEqual(red_dude, red_dude2)
        self.assertEqual(len(set([red_dude, red_dude2])), 1)  # yay, easily hashable

    def test_encode_metric(self):
        self.assertEqual(
            json.dumps(
                ExampleMetric(2.5, (1.5, 2, 0)),
                cls=MetricJsonEncoder,
                sort_keys=True,
            ),
            '{"__class__": "tests.utils.example_metrics.ExampleMetric", "momentum": [1.5, 2, 0], "speed": 2.5}'
        )

        self.assertEqual(
            json.dumps(
                ExampleMetric2(2.5, (1.5, 2, 0)),
                cls=MetricJsonEncoder,
                sort_keys=True,
            ),
            '{"__class__": "tests.utils.example_metrics.ExampleMetric2", "momentum": [1.5, 2, 0], "speed": 2.5, "violence": true}'
        )

        self.assertEqual(
            json.dumps(
                {'hello there': Grader().get_metric()},
                cls=MetricJsonEncoder,
                sort_keys=True,
            ),
            '{"hello there": null}'
        )

if __name__ == '__main__':
    unittest.main()
