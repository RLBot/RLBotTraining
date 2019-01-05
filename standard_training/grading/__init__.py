"""
This module exists to provide common types of gading for exercises
als allow composition of them.
"""
from .compound_grader import CompoundGrader
from .event_detector import PlayerEventDetector, PlayerEvent, PlayerEventType
from .goal_grader import StrikerGrader, GoalieGrader
from .grader import Grader
from .grader_exercise import GraderExercise
from .timeout import FailOnTimeout, PassOnTimeout
from .training_tick_packet import TrainingTickPacket
