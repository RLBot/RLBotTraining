import unittest
import json
from dataclasses import dataclass, field

from rlbottraining.history.metric import Metric

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

        @dataclass
        class CompositeRectangle(Rectangle):
            width: float = SpecificWidthRectangle.width
            height: float = SpecificHeightRectangle.height
        self.assertEqual(
            repr(CompositeRectangle()),
            'MetricsTest.test_dataclass_3.<locals>.CompositeRectangle(width=5, height=4)'
        )

        # A class with a nondefault may not override a dataclass with a default.
        try:
            @dataclass
            class Cuboid(Rectangle):
                depth: float
        except TypeError:
            pass
        else:
            self.fail()

if __name__ == '__main__':
    unittest.main()
