from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

import math

class LineGoalie(BaseAgent):
    """
    A goalie which tries to block the ball bymoving along a line parallel to the goals.
    A known weakness of this goalie bot is that it never comes out to challange the ball.
    """

    # Don't go too far outside the width of the goal.
    MAX_X = 4000
    MIN_X = -MAX_X

    MAX_Z = 800
    MIN_Z = 0

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        # Get the direction to the ball
        # car_obj = game_tick_packet.game_cars[self.index]
        # car = car_obj.physics
        # ball = game_tick_packet.game_ball.physics
        # if ball.velocity.z == 0:
        #     # Not moving towards to goal - no need to do stuff, right?
        #     return SimpleControllerState()
        # time_to_intercept = (car.location.y - ball.location.y) / ball.velocity.y

        # # A better bot would apply gravity and better ball physics in general.
        # # TODO: use RLBot ball prediction
        # intercept_x = ball.location.x + ball.velocity.x * time_to_intercept
        # intercept_x = min(self.MAX_X, max(self.MIN_X, intercept_x))
        # intercept_z = ball.location.z + ball.velocity.z * time_to_intercept
        # intercept_z = min(self.MAX_Z, max(self.MIN_Z, intercept_z))

        # # How is the car aligned with the direction to the ball?
        # yaw = float(car.physics.rotation.yaw)
        # car_forward_x = -math.sin(yaw)
        # car_left_y = math.cos(yaw)
        # dot_product = to_ball_x*car_left_x + to_ball_y*car_left_y
        self.render_ball_prediction()

        # Act on the information above.
        controller_state = SimpleControllerState()
        # controller_state.throttle = 1.0
        # controller_state.steer = min(1, max(-1, 5 * dot_product))
        # controller_state.boost = abs(dot_product) < .1
        # controller_state.handbrake = abs(dot_product) > .9
        return controller_state

    def render_ball_prediction(self):
        ball_prediction = self.get_ball_prediction_struct()

        if ball_prediction is None:
            print ('no ball pred')
            return

        self.renderer.begin_rendering('prediction')
        colors = [
            self.renderer.create_color(255, 255, 100, 100),
            self.renderer.create_color(255, 255, 255, 100),
            self.renderer.create_color(255, 100, 255, 100),
            self.renderer.create_color(255, 100, 255, 255),
            self.renderer.create_color(255, 100, 100, 255),
            self.renderer.create_color(255, 255, 100, 255)
        ]
        for i in range(0, ball_prediction.num_slices):
            current_slice = ball_prediction.slices[i].physics.location
            self.renderer.draw_rect_3d(current_slice, 8, 8, True, colors[i % len(colors)], True)
        self.renderer.end_rendering()



if __name__ == '__main__':
    # run_easy_exercises()
    # run_some_bakkesmod_exercises()
    agent = LineGoalie('name', 0, 0)
    print(agent.get_output(GameTickPacket()))
