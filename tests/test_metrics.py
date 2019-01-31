import unittest
import json
from dataclasses import dataclass, field

from rlbot.training.training import Pass, Fail, FailDueToExerciseException, Result

from rlbottraining.grading.grader import Grader
from rlbottraining.history.metric import Metric
from rlbottraining.history.metric_json_encoder import MetricJsonEncoder

from .utils.example_metrics import ExampleMetric, ExampleMetric2

def encode(obj):
    return json.dumps(
        obj,
        cls=MetricJsonEncoder,
        sort_keys=True,
    )

class MetricsTest(unittest.TestCase):


    def test_encode_metric(self):
        self.assertEqual(
            encode(ExampleMetric(2.5, (1.5, 2, 0))),
            '{"__class__": "tests.utils.example_metrics.ExampleMetric", "momentum": [1.5, 2, 0], "speed": 2.5}'
        )

    def test_encode_metric_inheritance(self):
        self.assertEqual(
            encode(ExampleMetric2(2.5, (1.5, 2, 0))),
            '{"__class__": "tests.utils.example_metrics.ExampleMetric2", "momentum": [1.5, 2, 0], "speed": 2.5, "violence": true}'
        )

    def test_encode_from_base_grader(self):
        self.assertEqual(
            encode({'hello there': Grader()}),
            '{"hello there": {"__class__": "rlbottraining.grading.grader.Grader"}}'
        )

    def test_encode_exception(self):
        ex = 'nope'
        try:
            1/0
        except Exception as e:
            ex = e
        else:
            self.fail()
        self.assertEqual(
            encode(ex),
            '{"__class__": "ZeroDivisionError", "__isinstance_Exception__": true, "message": "division by zero"}'
        )

    def test_encode_exception(self):
        ex = 'nope'
        try:
            1/0
        except Exception as e:
            ex = e
        else:
            self.fail()
        self.assertEqual(
            encode(ex),
            '{"__class__": "ZeroDivisionError", "__isinstance_Exception__": true, "message": "division by zero"}'
        )
    def test_encode_unencodable(self):
        self.assertEqual(
            encode({'foo': NonJsonEncodable()}),
            '{"foo": {"__encode_error__": {"__class__": "TypeError", "__isinstance_Exception__": true, "message": "Object of type NonJsonEncodable is not JSON serializable"}}}'
        )

    def test_encode_grade(self):
        self.assertEqual(
            encode(Fail()),
            '{"__class__": "rlbot.training.training.Fail", "__isinstance_Fail__": true}'
        )

    def test_encode_grade_FailDueToExerciseException(self):
        try:
            [1,2,3][15]
        except Exception as e:
            grade = FailDueToExerciseException(e, 'fake_traceback')
        self.assertEqual(
            encode(grade),
            '{"__class__": "rlbot.training.training.FailDueToExerciseException", "__isinstance_Fail__": true, "exception": {"__class__": "IndexError", "__isinstance_Exception__": true, "message": "list index out of range"}, "traceback_string": "fake_traceback"}'
        )

    def test_encode_grade_custom_subclass(self):
        @dataclass
        class MyPassPort(Pass):
            passport_number: str
        self.assertEqual(
            encode(MyPassPort(passport_number='lol jk')),
            '{"__class__": "tests.test_metrics.MyPassPort", "__isinstance_Pass__": true, "passport_number": "lol jk"}'
        )

    def test_encode_grade_custom_subclass_with_nonencodable(self):
        @dataclass
        class MyPassPort(Pass):
            passport_number: NonJsonEncodable
        self.assertEqual(
            encode(MyPassPort(passport_number=NonJsonEncodable())),
            '{"__class__": "tests.test_metrics.MyPassPort", "__isinstance_Pass__": true, "passport_number": {"__encode_error__": {"__class__": "TypeError", "__isinstance_Exception__": true, "message": "Object of type NonJsonEncodable is not JSON serializable"}}}'
        )

    # def test_encode_result(self):
    #     self.assertEqual(
    #         encode(Result()))

class NonJsonEncodable:
    def __init__(self):
        def dummy_function():
            pass
        self.function_property = dummy_function


if __name__ == '__main__':
    unittest.main()
