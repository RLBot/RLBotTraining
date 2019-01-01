from typing import Tuple
from enum import Enum

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.ball_prediction_struct import BallPrediction, Slice as BallPredictionSlice
from rlbot.utils.structures.game_data_struct import GameTickPacket

from math import tau, sin, cos, tan, copysign

def zero_centered_angle(theta:float) -> float:
    while theta > tau/2:
        theta -= tau
    return theta

def clamp(x, minimum=0, maximum=1):
    return min(maximum, max(minimum, x))

class LineGoalie(BaseAgent):
    """
    A goalie which tries to block the ball bymoving along a line parallel to the goals.
    A known weakness of this goalie bot is that it never comes out to challange the ball.
    """

    # How far away from the center of the car we should aim to intercept the ball.
    AIM_Z_DIST = 20

    # Don't go too far outside the width of the goal.
    MAX_X = 4000
    MIN_X = -MAX_X

    MAX_Z = 800
    MIN_Z = 0

    JUMP_BEFORE_INTERCEPT_SECONDS = .5

    class State(Enum):
        GROUND = 1

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:

        car_obj = game_tick_packet.game_cars[self.index]
        car = car_obj.physics

        # Find the time/position where we should intercept the ball.
        car_y = car.location.y
        to_ball_y = game_tick_packet.game_ball.physics.location.y - car_y
        intercept_y = car_y + copysign(self.AIM_Z_DIST, to_ball_y)
        prediction_struct = self.get_ball_prediction_struct()
        ball_intercept = prediction_struct.slices[0]
        for i, next_intercept in zip(range(prediction_struct.num_slices), prediction_struct.slices):
            if i == 0:
                continue
            if (
                abs(next_intercept.physics.location.y - intercept_y) <
                abs(ball_intercept.physics.location.y - intercept_y)
            ):
                ball_intercept = next_intercept
            else:
                # Do not search further: we do not care about backboard bounces which might come closer.
                break
        ball_intercept.physics.location.y = intercept_y

        seconds_until_jump = ball_intercept.game_seconds - game_tick_packet.game_info.seconds_elapsed - self.JUMP_BEFORE_INTERCEPT_SECONDS
        self.render_intercept(ball_intercept, seconds_until_jump)
        state = self.State.GROUND # TODO

        controller_state = SimpleControllerState()
        if state == self.State.GROUND:
            controller_state.throttle = (
                # PD-controller
                1.0 * (ball_intercept.physics.location.x - car.location.x) +
                0.3 * (0 - car.velocity.x)
            )
            controller_state.boost = controller_state.throttle > 200.

            car_yaw = zero_centered_angle(car.rotation.yaw)
            car_yaw_vel = car.angular_velocity.z
            controller_state.steer = (
                # PD-controller
                1.0 * (0 - car_yaw) +
                0.1 * (0 - car_yaw_vel)
            )
            if controller_state.throttle < 1:
                controller_state.steer *= -1

            controller_state.throttle = clamp(controller_state.throttle, -1, 1)
            controller_state.steer = clamp(controller_state.steer, -1, 1)

        else:
            self.logger.warn(f'invalid state {state}')
        return controller_state

    def render_intercept(self, ball_intercept: BallPredictionSlice, seconds_until_jump: float):
        self.renderer.begin_rendering('block intercept')
        location = ball_intercept.physics.location
        def vec3(x,z):
            return (
                location.x + x,
                location.y,
                location.z + z
            )
        self.renderer.draw_line_3d(vec3(-100., -100), vec3(-100, 100), self.renderer.red())
        self.renderer.draw_line_3d(vec3( 100., -100), vec3( 100, 100), self.renderer.red())
        # Draw a stop sign with an indication of time.
        sides = 8
        r = 40
        for i in range(sides):
            theta = tau*i/sides
            x = r * cos(theta) # center of polygon edge
            z = r * sin(theta)
            tx = -z * tan(.5*tau/sides) # tangent of edge
            tz = +x * tan(.5*tau/sides)
            outwards = max(1, 2 * seconds_until_jump +1)
            x *= outwards
            z *= outwards
            self.renderer.draw_line_3d(
                vec3(x+tx, z+tz),
                vec3(x-tx, z-tz),
                self.renderer.red()
            )

        # draw something in the center
        self.renderer.draw_rect_3d(location, 10, 10, True, self.renderer.white() if seconds_until_jump <= 0 else self.renderer.red(), True)
        self.renderer.end_rendering()

    def render_ball_prediction(self, ball_prediction: BallPrediction):

        self.renderer.begin_rendering('prediction')
        def get_color(i):
            colors = [
                self.renderer.create_color(255, 255, 100, 100),
                self.renderer.create_color(255, 255, 255, 100),
                self.renderer.create_color(255, 100, 255, 100),
                self.renderer.create_color(255, 100, 255, 255),
                self.renderer.create_color(255, 100, 100, 255),
                self.renderer.create_color(255, 255, 100, 255)
            ]
            return colors[i % len(colors)]
        step_size = 2
        for i in range(0, ball_prediction.num_slices, step_size):
            current_slice = ball_prediction.slices[i*step_size].physics.location
            self.renderer.draw_rect_3d(current_slice, 8, 8, True, get_color(i), True)
        self.renderer.end_rendering()
