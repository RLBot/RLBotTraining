from typing import Iterator, List
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
import random
import tempfile
import unittest

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.game_state_util import GameState

from rlbottraining.paths import _common_exercises_dir
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.grading.grader import Grader

from rlbot.utils.class_importer import load_external_module


class CommonExercisesQuickTest(unittest.TestCase):
    '''
    This test runs common exercises with their default configs
    and checks that, until they need to interact with RocketLeague,
    they behave as expected.
    '''

    def test_exercises_before_grading(self):
        for file in _common_exercises_dir.glob('**/*.py'):
            if file.name == 'ball_prediction.py':
                # Something is making the "python stopped working" dialog show up
                # even though it passes. Probably not cleaning something up properly.
                continue

            module = load_external_module(file)
            if not hasattr(module, 'make_default_playlist'):
                continue
            playlist = module.make_default_playlist()
            for ex in playlist:
                rng = SeededRandomNumberGenerator(Random(14))
                self.assertIsInstance(ex.match_config, MatchConfig)
                self.assertIsInstance(ex.grader, Grader)
                self.assertIsInstance(ex.make_game_state(rng), GameState)

if __name__ == '__main__':
    unittest.main()
