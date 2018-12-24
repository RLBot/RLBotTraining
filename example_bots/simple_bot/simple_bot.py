from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

import math

class SimpleBot(BaseAgent):

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        # Get the direction to the ball
        car = game_tick_packet.game_cars[self.index]
        ball_pos = game_tick_packet.game_ball.physics.location
        to_ball_x = ball_pos.x - car.physics.location.x
        to_ball_y = ball_pos.y - car.physics.location.y
        dist_to_ball = math.sqrt(to_ball_x**2 + to_ball_y**2)
        if dist_to_ball == 0: return SimpleControllerState()
        to_ball_x /= dist_to_ball
        to_ball_y /= dist_to_ball

        # How is the car aligned with the direction to the ball?
        yaw = float(car.physics.rotation.yaw)
        car_left_x = -math.sin(yaw)
        car_left_y = math.cos(yaw)
        dot_product = to_ball_x*car_left_x + to_ball_y*car_left_y

        # Act on the information above.
        controller_state = SimpleControllerState()
        controller_state.throttle = 1.0
        controller_state.steer = min(1, max(-1, 5 * dot_product))
        controller_state.boost = abs(dot_product) < .1
        controller_state.handbrake = abs(dot_product) > .9
        return controller_state
