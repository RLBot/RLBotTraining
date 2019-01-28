from dataclasses import dataclass, field

from rlbottraining.common_graders.goal_grader import StrikerGrader, GoalieGrader
from rlbottraining.training_exercise import TrainingExercise
from rlbottraining.grading.grader import Grader

"""
This module holds base classes which save us the line specifying the grader.
"""

@dataclass
class StrikerExercise(TrainingExercise):
    grader: Grader = field(default_factory=StrikerGrader)

@dataclass
class GoalieExercise(TrainingExercise):
    grader: Grader = field(default_factory=GoalieGrader)
