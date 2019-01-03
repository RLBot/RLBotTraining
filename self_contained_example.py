import math
import random
from os.path import join, dirname

from rlbot.training.training import Pass, Fail, Exercise, run_all_exercises
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

"""
This file is meant as an introduction to the features of the RLBot training interface.
This example deliberately does not drag in the the more complex control flow
that is used to define most of our other tests.
"""


class FailWithReason(Fail):
    def __init__(self, reason: str):
        self.reason = reason

    def __repr__(self) -> str:
        return f'{super().__repr__()}: {self.reason}'


class MoveToBall(Exercise):
    """
    This exercise tests that the bot drives towards a stationary ball.
    It assumes that the config specifies exactly one bot.
    """

    def __init__(
            self,
            player_location,
            player_rotation=Rotator(0, 0, 0),
            ball_location=Vector3(x=0, y=0, z=100),
            timeout_seconds=4.0):
        self.player_location = player_location
        self.player_rotation = player_rotation
        self.ball_location = ball_location
        self.timeout_seconds = timeout_seconds
        # These variables must be reset in setup() for repeated runs.
        self.init_dist_to_ball = None
        self.init_game_seconds = None

    def get_config_path(self) -> str:
        return join(dirname(__file__), 'rlbot_configs', 'single_soccar.cfg')

    def setup(self, rng: random.Random) -> GameState:
        self.init_dist_to_ball = None
        self.init_game_seconds = None
        return GameState(
            ball=BallState(physics=Physics(
                location=self.ball_location,
                velocity=Vector3(0, 0, 0),
                angular_velocity=Vector3(0, 0, 0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=self.player_location,
                        rotation=self.player_rotation,
                        velocity=Vector3(0, 0, 0),
                        angular_velocity=Vector3(0, 0, 0)),
                    jumped=False,
                    double_jumped=False,
                    boost_amount=0)
            },
            boosts={i: BoostState(0) for i in range(34)},
        )

    def on_tick(self, game_tick_packet: GameTickPacket):
        car_pos = game_tick_packet.game_cars[0].physics.location
        ball_pos = game_tick_packet.game_ball.physics.location
        to_ball_x = ball_pos.x - car_pos.x
        to_ball_y = ball_pos.y - car_pos.y
        dist_to_ball = math.sqrt(to_ball_x ** 2 + to_ball_y ** 2)

        # Did we drive to the ball?
        if self.init_dist_to_ball is None:
            self.init_dist_to_ball = dist_to_ball
        if dist_to_ball < 0.5 * self.init_dist_to_ball:
            return Pass()
        if dist_to_ball > 2.0 * self.init_dist_to_ball:
            return FailWithReason("Drove away from ball.")

        # timeout
        seconds_elapsed = game_tick_packet.game_info.seconds_elapsed
        if self.init_game_seconds is None:
            self.init_game_seconds = seconds_elapsed
        if seconds_elapsed - self.init_game_seconds > self.timeout_seconds:
            return FailWithReason(f"Hit the timout of {self.timeout_seconds} seconds")


class MoveBrickToBall(MoveToBall):
    """ Same as MoveToBall but now tests brickbot instead. """

    def get_config_path(self) -> str:
        return join(dirname(__file__), 'rlbot_configs', 'single_soccar_brick_bot.cfg')


def main():
    result_iter = run_all_exercises({
        'MoveToBall(From enemy side)': MoveToBall(Vector3(0, 4500, 0)),
        'MoveToBall(From own side)': MoveToBall(Vector3(0, -4500, 0)),
        'MoveToBall(From side wall)': MoveToBall(Vector3(-3000, 0, 0)),
        'MoveToBall(Medium Distance)': MoveToBall(Vector3(0, 2000, 0)),
        'MoveToBall(Near ball)': MoveToBall(Vector3(0, 500, 0)),
        'MoveToBall(01 When Facing towards ball)': MoveToBall(Vector3(-1500, 0, 0)),  # This one is expected to fail
        # These ones below are expected to fail.
        'MoveToBall(02 When Facing away from ball)': MoveToBall(Vector3(1500, 0, 0)),  # This one is expected to fail
        'MoveBrickToBall(From enemy side)': MoveBrickToBall(Vector3(0, 1500, 0)),
        'MoveBrickToBall(From own side)': MoveBrickToBall(Vector3(0, -1500, 0)),
    })

    # Note: results is an iterator, not a list. We can only do this for-loop once.
    num_failed = 0
    for name, result in result_iter:
        print(f'{name}: {result.grade}')
        if isinstance(result.grade, Fail):
            num_failed += 1

    if num_failed:
        print(f'{num_failed} exercises have been failed.')
    else:
        print('All exercises have been passed!')


if __name__ == '__main__':
    main()
