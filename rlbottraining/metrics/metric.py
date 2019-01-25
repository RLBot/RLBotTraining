from typing import Dict, Any

class Metric:
    """
    A Metric allows the outcome of a Grader(-Exercise) to be persisted and reviewed.
    A Metric may contain other Metric's.
    """

    def to_json(self) -> Dict[str, Any]:
        """
        Returns a JSON-serializable version of this object.
        Only necessary to override this if you hold a non-JSON-serializable
        object that is not supported by RLBotTraining's MetricJsonEncoder.
        """
        return self.__dict__.copy()
