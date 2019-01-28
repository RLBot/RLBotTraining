from dataclasses import dataclass

from rlbot.training.training import Grade
from rlbottraining.training_exercise import TrainingExercise

@dataclass
class ExerciseResult:

    seed: int
    grade: Grade
    exercise: TrainingExercise
    reproduce_key: str
