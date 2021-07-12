
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
import copy


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
        # Choose the importance of the grades.

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
        self.previous_ball = None

    class FailDueToGroundHit(Fail):
        def __init__(self):
            pass

        def __repr__(self):
            return f'{super().__repr__()}: Ball hit the ground'


    def set_previous_info(self, ball):
        self.previous_ball = copy.deepcopy(ball)

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        packet = tick.game_tick_packet
        ball = packet.game_ball.physics
        hit_ground = False

        if self.previous_ball is None:
            self.set_previous_info(ball)
            return None

        max_ang_vel = 5.9999601985025075  #Max angular velocity possible
        previous_angular_velocity_norm = math.sqrt(self.previous_ball.angular_velocity.x**2 +
                                                   self.previous_ball.angular_velocity.y**2 +
                                                   self.previous_ball.angular_velocity.z**2 )

        angular_velocity_norm = math.sqrt(ball.angular_velocity.x**2 +
                                          ball.angular_velocity.y**2 +
                                          ball.angular_velocity.z**2 )

        if ball.location.z <= 1900:  #Making sure it doesnt count the ceiling

            if ball.angular_velocity.x != self.previous_ball.angular_velocity.x or \
               ball.angular_velocity.y != self.previous_ball.angular_velocity.y or \
               ball.angular_velocity.z != self.previous_ball.angular_velocity.z:
                # If the ball hit anything its angular velocity will change in at least one axis
                if (previous_angular_velocity_norm or angular_velocity_norm) == max_ang_vel:
                    '''
                    Implement correct way of dealing with maximum angular velocity
                    angular velocity gets rescaled which may change an axis that truly did not change, only got rescaled
                    '''
                    #Todo: implement detection for this case
                    self.set_previous_info(ball)
                    return None

                elif self.previous_ball.angular_velocity.z == ball.angular_velocity.z:
                    '''
                    Ball hit a flat horizontal surface
                    this only changes angular velocity z 
                    we still have to deal with distingushing from a ground touch, or a bot touch
                    This will not hold true if the ball is being pushed on the ground by a bot.
                    Todo: detect pushing from bot
                    '''

                    if packet.game_ball.latest_touch.time_seconds >= (packet.game_info.seconds_elapsed - (2/60)):
                        '''
                        if there was a touch this tick the bot may be dribbling
                        '''
                        #Todo: distinguish dribble from pushing on ground.
                        #Todo: write tests to test pushing.
                        self.set_previous_info(ball)
                        return None
                    else:
                        hit_ground = True
                else:
                    '''
                    detect if is being pushed
                    '''
                    if packet.game_ball.latest_touch.time_seconds != packet.game_info.seconds_elapsed:
                        '''
                        ball not hit by a bot on this tick
                        '''
                        self.set_previous_info(ball)
                        return None
                    else:
                        '''
                        detect if its pushing along the ground or not
                        '''
                        #Todo: implement detection for this case
                        pass

            velocity_norm = math.sqrt(ball.velocity.x**2 +
                                      ball.velocity.y**2 +
                                      ball.velocity.z**2)


            previous_velocity_norm = math.sqrt(self.previous_ball.velocity.x ** 2 +
                                               self.previous_ball.velocity.y ** 2 +
                                               self.previous_ball.velocity.z ** 2 )
            if previous_velocity_norm == velocity_norm == 0:
                '''
                ball is stopped on ground
                '''
                hit_ground = True
        self.set_previous_info(ball)
        if hit_ground:
            return self.FailDueToGroundHit()
