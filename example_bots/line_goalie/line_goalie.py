from typing import Tuple
from enum import Enum
from collections import deque, Counter


from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.ball_prediction_struct import BallPrediction, Slice as BallPredictionSlice
from rlbot.utils.structures.game_data_struct import GameTickPacket

from math import tau, sin, cos, tan, copysign, sqrt

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

    JUMP_BEFORE_INTERCEPT_SECONDS = .55
    DODGE_BEFORE_INTERCEPT_SECONDS = .45


    class State(Enum):
        GROUND = 1
        JUMPING = 2
        DODGING = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # State de-noising:
        # Two out of the last 3 states (including the current state) must
        self.state_history = deque([self.State.GROUND] * 5)
        self.state_history_counter = Counter(self.state_history)
        self.ticks_in_dodge_state = 0

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

        seconds_until_intercept = ball_intercept.game_seconds - game_tick_packet.game_info.seconds_elapsed
        seconds_until_jump = seconds_until_intercept - self.JUMP_BEFORE_INTERCEPT_SECONDS
        seconds_until_doge = seconds_until_intercept - self.DODGE_BEFORE_INTERCEPT_SECONDS


        state = self.State.GROUND
        if car_obj.has_wheel_contact:
            if seconds_until_intercept < self.JUMP_BEFORE_INTERCEPT_SECONDS:
                state = self.State.JUMPING
            else:
                state = self.State.GROUND
        else:
            if seconds_until_intercept < self.DODGE_BEFORE_INTERCEPT_SECONDS:
                state = self.State.DODGING
            else:
                state = self.State.JUMPING
            state = self.State.DODGING

        assert state

        # De-noise state
        self.state_history_counter[self.state_history.popleft()] -= 1
        self.state_history_counter[state] += 1
        self.state_history.append(state)
        state = self.state_history_counter.most_common(1)[0][0]

        self.render(ball_intercept, seconds_until_intercept, state)

        if state != self.State.DODGING:
            self.ticks_in_dodge_state = 0

        controller_state = SimpleControllerState()
        forward_adjust = (
            # PD-controller
            1.0 * (ball_intercept.physics.location.x - car.location.x) +
            0.3 * (0 - car.velocity.x)
        )
        if state == self.State.GROUND:
            # Drive to ball_intercept.physics.location.x
            controller_state.throttle = forward_adjust
            controller_state.boost = controller_state.throttle > 200.

            # Try to stay aligned with the x axis.
            car_yaw = zero_centered_angle(car.rotation.yaw)
            car_yaw_vel = car.angular_velocity.z
            controller_state.steer = (
                # PD-controller
                1.0 * (0 - car_yaw) +
                0.1 * (0 - car_yaw_vel)
            )
            if controller_state.throttle < 1:
                controller_state.steer *= -1

        elif state == self.State.JUMPING:
            controller_state.jump = True
        elif state == self.State.DODGING:
            self.ticks_in_dodge_state += 1
            if self.ticks_in_dodge_state < 10:
                controller_state.jump = False
            elif self.ticks_in_dodge_state == 12:
                controller_state.roll = 1
                controller_state.pitch = -0.005*forward_adjust
                normalize = 1/sqrt(controller_state.roll**2 + controller_state.pitch**2)
                controller_state.roll *= normalize
                controller_state.pitch *= normalize
                if controller_state.roll < .4:
                    # if we really need to go forwards/back, don't go sideways at all
                     controller_state.roll = 0
                controller_state.jump = True
            else:
                controller_state.jump = False
        else:
            self.logger.warn(f'invalid state {state}')
        controller_state.throttle = clamp(controller_state.throttle, -1, 1)
        controller_state.steer = clamp(controller_state.steer, -1, 1)
        return controller_state

    def render(self, ball_intercept: BallPredictionSlice, seconds_until_intercept: float, state):
        self.renderer.begin_rendering('block intercept')
        location = ball_intercept.physics.location
        def vec3(x,z):
            return (
                location.x + x,
                location.y,
                location.z + z
            )

        # Draw a stop-sign octagon with an indication of time.
        sides = 8
        r = 40
        for i in range(sides):
            theta = tau*i/sides
            x = r * cos(theta) # center of polygon edge
            z = r * sin(theta)
            tx = -z * tan(.5*tau/sides) # tangent of edge
            tz = +x * tan(.5*tau/sides)
            outwards = 1 + max(0, 2 * (seconds_until_intercept - self.JUMP_BEFORE_INTERCEPT_SECONDS))
            x *= outwards
            z *= outwards
            self.renderer.draw_line_3d(
                vec3(x+tx, z+tz),
                vec3(x-tx, z-tz),
                self.renderer.red()
            )
            s = 1.1  # draw a slightly larger one as well.
            self.renderer.draw_line_3d(
                vec3(s*(x+tx), s*(z+tz)),
                vec3(s*(x-tx), s*(z-tz)),
                self.renderer.red()
            )

        # draw something in the center
        if state == self.State.GROUND: color_func = self.renderer.grey
        elif state == self.State.JUMPING: color_func = self.renderer.red
        elif state == self.State.DODGING: color_func = self.renderer.white
        else: color_func = self.renderer.orange
        self.renderer.draw_rect_3d(location, 10, 10, True, color_func(), True)
        self.renderer.end_rendering()
