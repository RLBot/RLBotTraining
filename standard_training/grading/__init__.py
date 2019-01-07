"""
This module exists to provide common types of gading for exercises
als allow composition of them.
"""

# Do not sort the imports alphabetically, the order matters above here.
from .event_detector import PlayerEventDetector, PlayerEvent, PlayerEventType
from .training_tick_packet import TrainingTickPacket
from .grader import Grader
from .grader_exercise import GraderExercise
from .compound_grader import CompoundGrader
from .timeout import FailOnTimeout, PassOnTimeout
from .goal_grader import StrikerGrader, GoalieGrader
