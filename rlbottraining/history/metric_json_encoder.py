import ctypes
from typing import Mapping, Any
import json
from datetime import datetime

from rlbot.training.training import Pass, Fail, Result

from rlbottraining.history.metric import Metric
from rlbottraining.grading.grader import Grader
from rlbot.matchconfig.match_config import MatchConfig
from rlbot.matchconfig.conversions import ConfigJsonEncoder

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
        well_known_types = [Pass, Fail, Result, Grader]
        for cls in well_known_types:
            if not isinstance(obj, cls):
                continue
            json_dict = json.loads(self.encode(obj.__dict__))
            json_dict['__class__'] = full_class_name_of(obj)
            json_dict[f'__isinstance_{cls.__name__}__'] = True
            return json_dict

        if isinstance(obj, ctypes.Structure):
            json_dict = json.loads(CtypesEncoder().encode(obj))
            json_dict['__class__'] = full_class_name_of(obj)
            return json_dict

        if isinstance(obj, datetime):
            return {
                '__class__': 'datetime.datetime',
                'iso8601': iso_format(obj),
            }

        # Numpy array. Not using isinstance to keep dependencies lean.
        if 'ndarray' in obj.__class__.__name__:
            return obj.tolist()

        # Exception (note: this is a thing they want to propagate, rather than an accident)
        if isinstance(obj, Exception):
            return jsonify_exception(obj)

        # Be permissive - propagate some things rather than failing to encode anything.
        # As a downside, we need to be more careful when reading these json objects back in
        # As an upside, we can diagnose what was wrong at a later point in time.
        if not hasattr(self, 'default_encoder'):
            self.default_encoder = ConfigJsonEncoder()
        try:
            return self.default_encoder.default(obj)
        except Exception as e:
            return make_encode_error(e)


def full_class_name_of(obj) -> str:
    return full_class_name(obj.__class__)
def full_class_name(cls: type) -> str:
    # https://stackoverflow.com/a/2020083
    assert isinstance(type(cls), type), f'Did you mean to use full_class_name_of() instead? type() returned {type(cls)}'
    module = cls.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__name__  # Avoid reporting __builtin__
    return module + '.' + cls.__name__

def iso_format(dt: datetime) -> str:
    try:
        utc = dt + dt.utcoffset()
    except TypeError as e:
        utc = dt
    isostring = datetime.strftime(utc, '%Y-%m-%dT%H:%M:%S.{0}Z')
    return isostring.format(int(round(utc.microsecond/1000.0)))

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


class CtypesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (ctypes.Array, list)):
            return [self.default(e) for e in obj]

        if isinstance(obj, ctypes._Pointer):
            return self.default(obj.contents) if obj else None

        if isinstance(obj, ctypes._SimpleCData):
            return self.default(obj.value)

        if isinstance(obj, (bool, int, float, str)):
            return obj

        if obj is None:
            return obj

        if isinstance(obj, (ctypes.Structure, ctypes.Union)):
            result = {}
            anonymous = getattr(obj, '_anonymous_', [])

            for key, *_ in getattr(obj, '_fields_', []):
                value = getattr(obj, key)

                # private fields don't encode
                if key.startswith('_'):
                    continue

                if key in anonymous:
                    result.update(self.default(value))
                else:
                    result[key] = self.default(value)

            return result

        return json.JSONEncoder.default(self, obj)
