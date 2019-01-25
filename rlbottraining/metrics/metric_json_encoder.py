from json import JSONEncoder

from .metric import Metric

class MetricJsonEncoder(JSONEncoder):
    def default(self, obj):
        # Metric
        if isinstance(obj, Metric):
            assert type(obj) != Metric, 'Must subclass Metric, not use it directly'
            json_dict = obj.to_json()
            # Tag our Metrics such that we can write specialized code to visualize them.
            assert '__class__' not in json_dict
            json_dict['__class__'] = full_class_name(obj)
            return json_dict

        # Numpy array. Not using isinstance to keep dependencies lean.
        if 'ndarray' in obj.__class__.__name__:
            return obj.tolist()

        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)

def full_class_name(obj):
    # https://stackoverflow.com/a/2020083
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__  # Avoid reporting __builtin__
    return module + '.' + obj.__class__.__name__
