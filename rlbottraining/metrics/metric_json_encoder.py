from typing import Mapping, Any
import json

from rlbot.training.training import Pass, Fail, Result, Exercise

from rlbottraining.metrics.metric import Metric
from rlbottraining.grading import GraderExercise, Grader


class MetricJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # Metric
        if isinstance(obj, Metric):
            assert type(obj) != Metric, 'Must subclass Metric, not use it directly'
            json_dict = obj.to_json()
            # Tag our Metrics such that we can write specialized code to visualize them.
            assert '__class__' not in json_dict
            json_dict['__class__'] = full_class_name_of(obj)
            return json_dict

        # Best-effort encoding of some well known types which could get subclassed.
        well_known_types = [Pass, Fail, Result, Exercise, GraderExercise, Grader]
        for cls in well_known_types:
            if not isinstance(obj, cls):
                continue
            json_dict = json.loads(self.encode(obj.__dict__))
            json_dict['__class__'] = full_class_name_of(obj)
            json_dict[f'__isinstance_{cls.__name__}__'] = True
            return json_dict

        # Numpy array. Not using isinstance to keep dependencies lean.
        if 'ndarray' in obj.__class__.__name__:
            return obj.tolist()

        # Exception (note: this is a thing they want to propagate, rather than an accident)
        if isinstance(obj, Exception):
            return jsonify_exception(obj)

        # Be permissive - propagate some things rather than failing to encode anything.
        # As a downside, we need to be more careful when reading these json objects back in
        # As an upside, we can diagnose what was wrong at a later point in time.
        try:
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)
        except Exception as e:
            return make_encode_error(e)




def full_class_name_of(obj) -> str:
    return full_class_name(obj.__class__)
def full_class_name(cls: type) -> str:
    # https://stackoverflow.com/a/2020083
    assert type(cls) is type, 'Did you mean to use full_class_name_of() instead?'
    module = cls.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__name__  # Avoid reporting __builtin__
    return module + '.' + cls.__name__


def jsonify_exception(e: Exception):
    return {
        '__class__': full_class_name_of(e),
        '__isinstance_Exception__': True,
        'message': str(e),
    }

def make_encode_error(e: Exception):
    return {
        '__encode_error__': jsonify_exception(e)
    }
