from os.path import join, dirname
import random
import math

from rlbot.training.training import Pass, Fail, Exercise, run_all_exercises
from rlbot.utils.game_state_util import GameState, BoostState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

class MoveToBall(Exercise):

    def __init__(self, dist_to_ball):
        self.init_dist_to_ball = dist_to_ball

    def get_config_path(self) -> str:
        return join(dirname(__file__), 'rlbot_configs', 'single_soccar.cfg')

    def setup(self, rng: random.Random) -> GameState:
        return GameState(
            ball=BallState(physics=Physics(
                location=Vector3(x=0, y=0, z=100),
                velocity=Vector3(0,0,0),
                angular_velocity=Vector3(0,0,0))),
            cars={
                0: CarState(
                    physics=Physics(
                        location=Vector3(x=-self.init_dist_to_ball, y=0, z=0), 
                        rotation=Rotator(0, 0, 0),
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
        horizontal_dist = math.sqrt(car_pos.x**2 + car_pos.y**2)
        if horizontal_dist < 0.5 * self.init_dist_to_ball:
            return Pass()
        if horizontal_dist > 2.0 * self.init_dist_to_ball:
            return Fail()
        # TODO: timeout

def main():
    result_iter = run_all_exercises({
        "Moves to ball when close": MoveToBall(500),
        # "Moves to ball when far": MoveToBall(600),
        "Z 0": MoveToBall(3000),
        "Z 1": MoveToBall(3001),
        "Z 2": MoveToBall(3002),
        "Z 3": MoveToBall(3003),
        "Z 4": MoveToBall(3004),
        "Z 5": MoveToBall(3005),
        "Z 6": MoveToBall(3006),
        "Z 7": MoveToBall(3007),
        "Z 8": MoveToBall(3008),
        "Z 9": MoveToBall(3009),
    })

    # Note: results is an iterator, not a list. We can only do this for-loop once.
    num_failed = 0
    for name, result in result_iter:
        print(f'{name}: {str(result.grade)}')
        if isinstance(result.grade, Fail):
            num_failed += 1

    if num_failed:
        print(f'{num_failed} exercises have been failed.')
    else:
        print('All excercises have been passed!')

if __name__ == '__main__':
    main()
