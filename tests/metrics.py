import unittest
import json
from dataclasses import dataclass

from rlbot.training.training import Pass, Fail, FailDueToExerciseException, Result

from rlbottraining.grading.grader import Grader
from rlbottraining.metrics.metric import Metric
from rlbottraining.metrics.metric_json_encoder import MetricJsonEncoder

from .utils.example_metrics import ExampleMetric, ExampleMetric2

def encode(obj):
    return json.dumps(
        obj,
        cls=MetricJsonEncoder,
        sort_keys=True,
    )

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

    def test_dataclass_2(self):
        class NonDataClassBase:
            foo:int = 3
            def __init__(self, bar):
                self.bar = bar
                pass
        @dataclass
        class Rectangle(NonDataClassBase):
            width: float
            height: float
        rect = Rectangle(3,4)
        self.assertEqual(repr(rect), 'MetricsTest.test_dataclass_2.<locals>.Rectangle(width=3, height=4)')
        self.assertTrue(hasattr(rect, 'foo'))
        self.assertFalse(hasattr(rect, 'bar'))
        class Cuboid(Rectangle):
            def __init__(self, width, height, depth):
                super().__init__(width, height)
                self.depth = depth
        cube = Cuboid(1,2,3)
        self.assertEqual(cube.width, 1)
        self.assertEqual(cube.height, 2)
        self.assertEqual(cube.depth, 3)

    def test_dataclass_3(self):
        '''
        Check how overriding default values works.
        '''
        @dataclass
        class Rectangle:
            width: float = 0
            height: float = 0
        @dataclass
        class SpecificWidthRectangle(Rectangle):
            width: float = 5
            specificWidth: bool = True

        self.assertEqual(
            # Same argument-order as Rectangle
            repr(SpecificWidthRectangle(3)),
            'MetricsTest.test_dataclass_3.<locals>.SpecificWidthRectangle(width=3, height=0, specificWidth=True)'
        )
        self.assertEqual(
            repr(SpecificWidthRectangle(height=3)),
            'MetricsTest.test_dataclass_3.<locals>.SpecificWidthRectangle(width=5, height=3, specificWidth=True)'
        )
        self.assertEqual(
            SpecificWidthRectangle(3).__dict__,
            {'width': 3, 'height': 0, 'specificWidth': True}
        )

        @dataclass
        class SpecificHeightRectangle(Rectangle):
            height: float = 4
            specificHeight: bool = True

        '''
        How does diamond-shaped multiple-inheritance work?
        It grabs the overriding defauls of one, including its base class.
        '''
        @dataclass
        class SpecificWidthHeightRectangle(SpecificWidthRectangle, SpecificHeightRectangle):
            pass
        self.assertEqual(
            repr(SpecificWidthHeightRectangle()),
            'MetricsTest.test_dataclass_3.<locals>.SpecificWidthHeightRectangle(width=5, height=0, specificHeight=True, specificWidth=True)'
        )


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
            encode({'hello there': Grader().get_metric()}),
            '{"hello there": null}'
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
            '{"__class__": "tests.metrics.MyPassPort", "__isinstance_Pass__": true, "passport_number": "lol jk"}'
        )

    def test_encode_grade_custom_subclass_with_nonencodable(self):
        @dataclass
        class MyPassPort(Pass):
            passport_number: NonJsonEncodable
        self.assertEqual(
            encode(MyPassPort(passport_number=NonJsonEncodable())),
            '{"__class__": "tests.metrics.MyPassPort", "__isinstance_Pass__": true, "passport_number": {"__encode_error__": {"__class__": "TypeError", "__isinstance_Exception__": true, "message": "Object of type NonJsonEncodable is not JSON serializable"}}}'
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
