import unittest
from dataclasses import dataclass, field
from typing import Optional, Callable, Mapping

import numpy as np
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.matchcomms.common_uses.set_attributes_message import make_set_attributes_message
from rlbot.matchcomms.common_uses.reply import send_and_wait_for_replies
from rlbot.training.training import Grade, Pass, Fail
from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.logging_utils import get_logger
from rlbot.setup_manager import setup_manager_context

from rlbottraining.training_exercise import TrainingExercise
from rlbottraining.paths import BotConfigs
from rlbottraining.common_exercises.common_base_exercises import StrikerExercise
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.common_graders.goal_grader import StrikerGrader
from rlbottraining.grading.grader import Grader
from rlbottraining.exercise_runner import run_playlist
from rlbottraining.match_configs import make_match_config_with_bots
from rlbottraining.common_graders.tick_wrapper import GameTickPacketWrapperGrader

@dataclass
class TurnAndDriveToBall(TrainingExercise):
    steering_coefficient: float = 5

    grader: Grader = field(default_factory=lambda: GameTickPacketWrapperGrader(
        StrikerGrader(timeout_seconds=4.0, ally_team=0)))

    match_config: MatchConfig = field(default_factory=lambda:
        make_match_config_with_bots(blue_bots=[BotConfigs.tweaked_bot]))


    def on_briefing(self) -> Optional[Grade]:
        _ = send_and_wait_for_replies(self.get_matchcomms(), [
            make_set_attributes_message(0, {'steering_coefficient': self.steering_coefficient}),
        ])

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(0, 5100, 100),
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(0, 3400, 0),
                        rotation=Rotator(0, 0, 0),
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

@dataclass
class FunctionOptimizationResult:
    best_input: float
    best_output: float
    all_samples: Mapping[float, float]  # x -> f(x)

def naive_function_minimization(
        f: Callable[[float], float], min_x: float, max_x: float,
        num_iterations: int=2, num_samples_each_iteration: int=9
    ) -> FunctionOptimizationResult:
    """
    Tries to find a local minimum of the function f(x)
    within the range min_x..max_x by sampling f(x).
    Returns the x for which f(x) gave the lowest value.

    Each iteration, it does a few samples between min_x and max_x
    then adjusts those to be around the best sample.
    """
    assert num_iterations > 0

    all_samples = dict()
    def f_memoized(x: float) -> float:
        if x not in all_samples:
            all_samples[float(x)] = f(x)
        return all_samples[x]

    best_x = None
    for iteration in range(num_iterations):
        domain = np.linspace(min_x, max_x, num=num_samples_each_iteration)
        samples = [f_memoized(x) for x in domain]
        _, best_i = min((fx, i) for i,fx in enumerate(samples))
        best_x = domain[best_i]
        min_x = domain[max(best_i-1, 0)]
        max_x = domain[min(best_i+1, len(domain)-1)]

    return FunctionOptimizationResult(
        best_input=best_x,
        best_output=all_samples[best_x],
        all_samples=all_samples,
    )


class TweakTest(unittest.TestCase):

    def test_on_briefing_tweak(self):
        logger = get_logger('steering optimization')
        # We want to assert that this constant is better than other constants.

        # Hold the setup_manager here such that we don't need to shutdown/relaunch everything all the time.
        with setup_manager_context() as setup_manager:
            def time_to_goal(steering_coefficient: float) -> float:
                ex = TurnAndDriveToBall(
                    name=f'Turn to ball (steering_coefficient={steering_coefficient:.2f})',
                    steering_coefficient=steering_coefficient
                )
                result = list(run_playlist([ex], setup_manager=setup_manager))[0]
                grade = result.grade
                assert isinstance(grade, GameTickPacketWrapperGrader.WrappedPass) or isinstance(grade, GameTickPacketWrapperGrader.WrappedFail), f'Unexpected grade: {grade}'
                duration_seconds = grade.last_tick.game_info.seconds_elapsed - grade.first_tick.game_info.seconds_elapsed
                logger.debug(f'intermediate result: {duration_seconds}')
                return duration_seconds
            result = naive_function_minimization(time_to_goal, .4, 9)

        logger.debug('Best steering_coefficient: ', result.best_input)
        logger.debug('all_samples:')
        for k,v in sorted(result.all_samples.items()):
            logger.debug(f'{k},{v}')
        self.assertLess(0.4, result.best_input)
        self.assertLess(1.0, result.best_output)
        self.assertLess(result.best_output, 4.0)

def make_default_playlist():
    return [TurnAndDriveToBall(name='Turn to ball', steering_coefficient=4.)]

if __name__ == '__main__':
    unittest.main()
