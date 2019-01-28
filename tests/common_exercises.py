import random
import unittest
from dataclasses import dataclass, field
import tempfile
from pathlib import Path

from rlbottraining.paths import _common_exercises_dir
from rlbottraining.exercise_runner import run_playlist

class CommonExercisesTest(unittest.TestCase):
    '''
    This test runs common exercises with their default configs
    and checks that they perform as expected.
    '''

    def test_ball_prediction(self):
        from rlbottraining.common_exercises.ball_prediction import make_default_playlist
        results = list(run_playlist(make_default_playlist()))
