
"""
This module contains graders which mimic the the behaviour of Rocket League custom training.
"""

import math

from dataclasses import dataclass
from typing import Optional, Mapping, Union

from rlbot.training.training import Pass, Fail, Grade

from rlbottraining.grading.grader import Grader
from rlbottraining.grading.event_detector import PlayerEventType
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.compound_grader import CompoundGrader
from rlbottraining.common_graders.timeout import FailOnTimeout, PassOnTimeout
from rlbottraining.common_graders.goal_grader import PassOnGoalForAllyTeam
from rlbot.training.training import Pass, Fail, Grade


class RocketLeagueStrikerGrader(CompoundGrader):
    """
    A Grader which aims to match the striker training.
    """

    def __init__(self, timeout_seconds=4.0, ally_team=0, timeout_override=False, ground_override=False):
        self.timeout_override = timeout_override
        self.ground_override = ground_override
        super().__init__([
            PassOnGoalForAllyTeam(ally_team),
            FailOnBallOnGround(),
            FailOnTimeout(timeout_seconds),
        ])

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        grades = [grader.on_tick(tick) for grader in self.graders]
        return self.grade_chooser(grades)

    def grade_chooser(self, grades) -> Optional[Grade]:
        """
        Chooses the importance of the grades
        """

        timeout = isinstance(grades[2], Fail)  # True if timed out, false otherwise
        ball_on_ground = isinstance(grades[1], Fail)  # True if ball touched the ground, false otherwise
        goal = isinstance(grades[0], Pass)  # True if ball there was a goal, false otherwise

        if goal:  # scoring and touching the ground on the same tick prefer scoring
            return grades[0]
        elif timeout:
            if self.timeout_override:
                return grades[2]
            elif ball_on_ground:
                return grades[1]
        elif self.ground_override and ball_on_ground:
            return grades[1]
        return None


class FailOnBallOnGround(Grader):
    def __init__(self):
        self.previous_ang_x = None
        self.previous_ang_y = None
        self.previous_ang_z = None
        self.previous_total_goals = None

    class FailDueToGroundHit(Fail):
        def __init__(self):
            pass

        def __repr__(self):
            return f'{super().__repr__()}: Ball hit the ground'


    def set_previous_angular_velocity(self, ball, reset = False):
        if not reset:
            self.previous_ang_x = ball.angular_velocity.x
            self.previous_ang_y = ball.angular_velocity.y
            self.previous_ang_z = ball.angular_velocity.z
            self.previous_vel_z = ball.velocity.z
        else:
            self.previous_ang_x = None
            self.previous_ang_y = None
            self.previous_ang_z = None
            self.previous_vel_z = None

    def set_previous_total_goals(self, total_goals, reset=False):
        if not reset:
            self.previous_total_goals = total_goals
        else:
            self.previous_total_goals = None

    def current_total_goals(self, packet):
        total_goals = 0
        for car_id in range(packet.num_cars):
            goal = packet.game_cars[car_id].score_info.goals
            own_goal = packet.game_cars[car_id].score_info.own_goals
            total_goals += goal + own_goal
        return total_goals

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        ball = tick.game_tick_packet.game_ball.physics
        hit_ground = False

        if self.previous_ang_z is None:
            self.set_previous_angular_velocity(ball)
        else:
            max_ang_vel = 5.9999601985025075  #Max angular velocity possible
            previous_ang_norm = math.sqrt(self.previous_ang_x**2 + self.previous_ang_y**2 + self.previous_ang_z**2)
            if ball.location.z <= 1900:  #Making sure it doesnt count the ceiling
                if (ball.angular_velocity.x != self.previous_ang_x or ball.angular_velocity.y != self.previous_ang_y):
                    # If the ball hit anything its angular velocity will change in the x or y axis
                    if self.previous_ang_z == ball.angular_velocity.z and not ( 130 < ball.location.z < 150) :
                        # if the z angular velocity did not change it means it was a flat plane.
                        #ignore dribbling
                        hit_ground = True
                    elif previous_ang_norm == max_ang_vel:
                        # if it was at maximum angular velocity, it may have changed z axis not to exceed max
                        # fallback on old behaviour
                        if ball.location.z < 100 and ball.velocity.z >= 0:
                            hit_ground = True
                    if ball.location.z <= 93.5 and ball.velocity.z >= 0:
                        # if the car is pushing the ball on the ground
                        hit_ground = True
        if math.sqrt(ball.velocity.x**2 + ball.velocity.y**2 + ball.velocity.z**2) == 0 and self.previous_vel_z != 0:
            # ball is stop on ground and not on its apex, which means it should fail anyway
            if self.previous_total_goals != self.current_total_goals(tick.game_tick_packet):
                # There was a goal, let the goal handler handle it
                hit_ground = False
            else:
                hit_ground = True

        self.set_previous_angular_velocity(ball)
        self.set_previous_total_goals(self.current_total_goals(tick.game_tick_packet))
        if hit_ground:
            self.set_previous_angular_velocity(ball, reset = True)
            return self.FailDueToGroundHit()
