import ctypes
from typing import Tuple
from enum import Enum
from collections import deque, Counter
from contextlib import contextmanager
from math import pi


from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.ball_prediction_struct import BallPrediction, Slice as BallPredictionSlice
from rlbot.utils.structures.game_data_struct import GameTickPacket, Vector3

from math import tau, sin, cos, tan, copysign, sqrt



def zero_centered_angle(theta:float) -> float:
    while theta > tau/2:
        theta -= tau
    return theta

def clamp(x, minimum=0, maximum=1):
    return min(maximum, max(minimum, x))

def distance(a: Vector3, b: Vector3):
    """
    Returns the euclidian distance between @a and @b
    TODO: use a shared library for this.
    """
    return sqrt(
        (a.x - b.x)**2 +
        (a.y - b.y)**2 +
        (a.z - b.z)**2
    )

def obj_distance(a, b):
    """
    Returns the distance between two objects which have a "physics" (type Physics) property.
    """
    return distance(a.physics.location, b.physics.location)

class StateDiscontinuityDetector:

    # https://youtu.be/0qw1xFv7Sv0
    MAX_PLAUSIBLE_BALL_SPEED = 15000 # uu/s

    def __init__(self):
        self.prev_tick_packet = None
    def is_discontinuous(self, game_tick_packet: GameTickPacket) -> bool:
        """
        Returns true iff it is implausible that we arrived at the current
        game_tick_packet by just waiting.
        Compares to the last time this function has been called.
        """
        with self._update_prev_on_return(game_tick_packet):
            if self.prev_tick_packet is None:
                self.prev_tick_packet = GameTickPacket()
                return False # Be on the safe side - On the first tick things are ok.
            dt = game_tick_packet.game_info.seconds_elapsed - self.prev_tick_packet.game_info.seconds_elapsed
            if dt == 0:
                return False
            ball_dist = obj_distance(game_tick_packet.game_ball, self.prev_tick_packet.game_ball)
            ball_speed = ball_dist / dt
            # TODO: detect it on other things as well. e.g. cars, gametime.
            return ball_speed > self.MAX_PLAUSIBLE_BALL_SPEED

    @contextmanager
    def _update_prev_on_return(self, game_tick_packet: GameTickPacket):
        yield  # body of `with` statement
        ctypes.pointer(self.prev_tick_packet)[0] = game_tick_packet  # make a copy with memcpy


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
    HEIGHT_BEFORE_DODGING = 50

    MIN_HIGH_JUMP_Z = 200  # minumum height of the predicted ball to get into the HIGH_JUMP state.
    MAX_HIGH_JUMP_Z = 630  # When not to jump at all because the ball it soo hightg

    DESIRED_OFFSET_FROM_OWN_GOAL_Y = 100

    class State(Enum):
        GROUND = 1
        JUMPING = 2
        DODGING = 3
        IDLE = 4
        HIGH_JUMP = 5
        HIGH_JUMP_GROUND = 6
    assert len(State) == len(State.__members__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_detector = StateDiscontinuityDetector()
        self.reset_state()

    def reset_state(self):
        self.ticks_in_dodge_state = 0
        # State de-noising:
        self.state_history = deque([self.State.GROUND] * 5)
        self.state_history_counter = Counter(self.state_history)

    def high_jump_before_intercept(self, predicted_ball_z: float) -> float:
        """
        Returns how long the high jump maneuver needs to be triggered before the intercept
        """
        return min(.99, predicted_ball_z/600.)

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:

        if self.reset_detector.is_discontinuous(game_tick_packet):
            self.reset_state()

        car_obj = game_tick_packet.game_cars[self.index]
        car = car_obj.physics

        # Find the time/position where we should intercept the ball.
        car_y = car.location.y
        to_ball_y = game_tick_packet.game_ball.physics.location.y - car_y
        intercept_y = car_y + copysign(self.AIM_Z_DIST, to_ball_y)
        prediction_struct = self.get_ball_prediction_struct()
        ball_intercept = prediction_struct.slices[0]
        for i, next_intercept in zip(range(prediction_struct.num_slices), prediction_struct.slices):
            if i == 0 or i == 1:
                continue
            if (
                abs(next_intercept.physics.location.y - intercept_y) <
                abs(ball_intercept.physics.location.y - intercept_y)
            ):
                ball_intercept = next_intercept
            else:
                # Do not search further: we do not care about backboard bounces which might come closer.
                break
        is_travelling_towards_line = ball_intercept.physics.velocity.y * to_ball_y < 0
        ball_intercept.physics.location.y = intercept_y

        seconds_until_intercept = ball_intercept.game_seconds - game_tick_packet.game_info.seconds_elapsed
        seconds_until_jump = seconds_until_intercept - self.JUMP_BEFORE_INTERCEPT_SECONDS
        seconds_until_doge = seconds_until_intercept - self.DODGE_BEFORE_INTERCEPT_SECONDS

        state = self.State.GROUND
        if car_obj.has_wheel_contact:
            if is_travelling_towards_line:
                if ball_intercept.physics.location.z > self.MAX_HIGH_JUMP_Z:
                    state = self.State.IDLE
                if ball_intercept.physics.location.z > self.MIN_HIGH_JUMP_Z:
                    if seconds_until_intercept < self.high_jump_before_intercept(ball_intercept.physics.location.z):
                        state = self.State.HIGH_JUMP
                    else:
                        state = self.State.HIGH_JUMP_GROUND
                else:
                    if seconds_until_intercept < self.JUMP_BEFORE_INTERCEPT_SECONDS:
                        state = self.State.JUMPING
                    else:
                        state = self.State.GROUND
            else:
                state = self.State.IDLE
        else:
            if not is_travelling_towards_line:
                state = self.State.IDLE
            elif ball_intercept.physics.location.z > self.MIN_HIGH_JUMP_Z:
                state = self.State.HIGH_JUMP
            else:
                if car.location.z <= self.HEIGHT_BEFORE_DODGING:
                    state = self.State.JUMPING
                elif car_obj.double_jumped:
                    state = self.State.IDLE
                else:
                    state = self.State.DODGING

        assert state

        to_enemy_goal_y = 1 if self.team == 0 else -1
        desired_car_y = -5120 * to_enemy_goal_y + self.DESIRED_OFFSET_FROM_OWN_GOAL_Y * to_enemy_goal_y
        self.render_horizontal_line(desired_car_y, self.MIN_HIGH_JUMP_Z)

        # De-noise state
        self.state_history_counter[self.state_history.popleft()] -= 1
        self.state_history_counter[state] += 1
        self.state_history.append(state)
        state = self.state_history_counter.most_common(1)[0][0]

        if state != self.State.DODGING:
            self.ticks_in_dodge_state = 0
        controller_state = SimpleControllerState()

        def forward_adjust(desired_x):
            return (
                # PD-controller
                1.0 * (desired_x - car.location.x) +
                0.3 * (0 - car.velocity.x)
            )

        if state == self.State.GROUND:
            # Drive to ball_intercept.physics.location.x
            controller_state.throttle = forward_adjust(ball_intercept.physics.location.x)
            controller_state.boost = controller_state.throttle > 200.

        elif state == self.State.JUMPING:
            controller_state.jump = True

        elif state == self.State.DODGING:
            self.ticks_in_dodge_state += 1
            if self.ticks_in_dodge_state < 2:
                controller_state.jump = False
            elif self.ticks_in_dodge_state == 3:
                controller_state.roll = 1
                controller_state.pitch = -0.008*forward_adjust(ball_intercept.physics.location.x)
                normalize = 1/sqrt(controller_state.roll**2 + controller_state.pitch**2)
                controller_state.roll *= normalize
                controller_state.pitch *= normalize
                if controller_state.roll < .4:
                    # if we really need to go forwards/back, don't go sideways at all
                     controller_state.roll = 0
                controller_state.jump = True
            else:
                controller_state.jump = False

        elif state == self.State.IDLE:
            desired_car_x = 0.4 * game_tick_packet.game_ball.physics.location.x
            controller_state.throttle = forward_adjust(desired_car_x)
            is_close_x = abs(car.location.x - desired_car_x) < 50
            if is_close_x and game_tick_packet.game_info.seconds_elapsed % 1 < .5:
                controller_state.throttle = -1
            # Try to stay aligned with the x axis.
            car_yaw = zero_centered_angle(car.rotation.yaw)
            to_desired_car_y = desired_car_y - car.location.y
            desired_yaw = min(pi/3, max(-pi/3, 0.004 * to_desired_car_y))
            if desired_car_x < car.location.x:
                desired_yaw *= -1

            car_yaw_vel = car.angular_velocity.z
            controller_state.steer = ( # PD-controller
                5.0 * (desired_yaw - car_yaw) +
                0.1 * (0 - car_yaw_vel)
            )
            if controller_state.throttle < 1:
                controller_state.steer *= -1
            if not car_obj.has_wheel_contact:
                # Hacky pitch/yaw/roll control. See NomBot for a better implementation.
                # Only works because desired rotation vector is (0,0,0).
                controller_state.pitch = -4 * car.rotation.pitch
                controller_state.yaw   = -4 * car.rotation.yaw
                controller_state.roll  = -5 * car.rotation.roll
                controller_state.pitch = min(1, max(-1, controller_state.pitch))
                controller_state.roll  = min(1, max(-1, controller_state.roll))
                controller_state.yaw   = min(1, max(-1, controller_state.yaw))

            # asign stuff just for rendering.
            seconds_until_intercept = 2.5
            ball_intercept.physics.location.x = desired_car_x
            ball_intercept.physics.location.z = 100

        elif state == self.State.HIGH_JUMP:
            z = car.location.z
            controller_state.jump = not (110 < z < 120)
            if car_obj.double_jumped:
                controller_state.pitch = min(1, max(-1, 5*(.9-car.rotation.pitch)))

        elif state == self.State.HIGH_JUMP_GROUND:
            if seconds_until_intercept == 0:
                desired_vel_x = 0  # avoid division by zero
            else:
                desired_vel_x = (ball_intercept.physics.location.x - car.location.x) / seconds_until_intercept
                desired_vel_x *= 1.1
            controller_state.throttle = (desired_vel_x - car.velocity.x)

        else:
            self.logger.warn(f'invalid state {state}')

        controller_state.throttle = clamp(controller_state.throttle, -1, 1)
        controller_state.steer = clamp(controller_state.steer, -1, 1)

        self.render_ball_intercept(ball_intercept, seconds_until_intercept, state)

        return controller_state

    def render_ball_intercept(self, ball_intercept: BallPredictionSlice, seconds_until_intercept: float, state):
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
        elif state == self.State.IDLE: color_func = self.renderer.green
        elif state == self.State.HIGH_JUMP_GROUND: color_func = lambda: self.renderer.create_color(255, 70, 70, 255)
        elif state == self.State.HIGH_JUMP: color_func = self.renderer.blue
        else: color_func = self.renderer.orange
        self.renderer.draw_rect_3d(location, 10, 10, True, color_func(), True)
        self.renderer.end_rendering()

    def render_horizontal_line(self, y, z, x_min=-900, x_max=900):
        self.renderer.begin_rendering()
        self.renderer.draw_line_3d([x_min, y+ 0, z], [x_max, y+ 0, z], self.renderer.create_color(200, 10, 255, 10))
        self.renderer.draw_line_3d([x_min, y+20, z], [x_max, y+20, z], self.renderer.create_color(200, 10, 255, 10))
        self.renderer.draw_line_3d([x_min, y-20, z], [x_max, y-20, z], self.renderer.create_color(200, 10, 255, 10))
        self.renderer.end_rendering()
