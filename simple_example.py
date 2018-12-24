from os.path import join, dirname
import random
import math

from rlbot.training.training import Pass, Fail, Exercise, run_all_exercises
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

class MoveToBall(Exercise):

    def __init__(self, player_location, player_rotation=Rotator(0, 0, 0), ball_location=Vector3(x=0,y=0,z=100)):
        self.player_location = player_location
        self.player_rotation = player_rotation
        self.ball_location = ball_location
        self.init_dist_to_ball = None

    def get_config_path(self) -> str:
        return join(dirname(__file__), 'rlbot_configs', 'single_soccar.cfg')

    def setup(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=self.ball_location,
                velocity=Vector3(0,0,0),
                angular_velocity=Vector3(0,0,0))),
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
        dist_to_ball = math.sqrt(to_ball_x**2 + to_ball_y**2)

        if self.init_dist_to_ball is None:
            self.init_dist_to_ball = dist_to_ball
            return
        if dist_to_ball < 0.5 * self.init_dist_to_ball:
            return Pass()
        if dist_to_ball > 2.0 * self.init_dist_to_ball:
            return Fail()
        # TODO: timeout

def main():
    result_iter = run_all_exercises({
        "00 From side": MoveToBall(Vector3(-3000, 0, 0)),
        "01 Facing away": MoveToBall(Vector3(1500, 0, 0)),  # This one is expected to fail
        "02 From own side": MoveToBall(Vector3(0, -4500, 0)),
        "03 From enemy side": MoveToBall(Vector3(0, 4500, 0)),
        "04 Medium Distance": MoveToBall(Vector3(0, 2000, 0)),
        "05 Close": MoveToBall(Vector3(0, 500, 0)),
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
        print('All excercises have been passed!')

if __name__ == '__main__':
    main()
