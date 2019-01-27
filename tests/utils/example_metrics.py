from dataclasses import dataclass
from typing import Tuple

from rlbottraining.history.metric import Metric

@dataclass(frozen=True)
class ExampleMetric(Metric):
    speed: float
    momentum: Tuple[float]

@dataclass(frozen=True)
class ExampleMetric2(ExampleMetric):
    violence: bool = True

