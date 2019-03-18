import json
from typing import Any, List, Dict, Union

Json = Any
JsonObject = Dict[str, Any]

def get_nested(obj: JsonObject, key_path: Union[List[str], str], default=None):
    if type(key_path) is str:
        key_path = key_path.split('.')

    try:
        for key in key_path:
            obj = obj[key]
    except KeyError:
        return default
    return obj

def set_nested(out_json, key_path: List[str], value):
    key, *remaining_key_path = key_path
    if len(remaining_key_path) == 0:
        out_json[key] = value
        return
    if key in out_json:
        subobject = out_json[key]
        assert isinstance(subobject, dict)
    else:
        subobject = {}
        out_json[key] = subobject
    set_nested(subobject, remaining_key_path, value)

def slim_copy(in_json: JsonObject, key_paths: List[List[str]]) -> JsonObject:
    """
    Returns a copy of @in_json where only paths
    specified by @keys_paths are copied.
    """
    out_json = {}
    for key_path in key_paths:
        value = get_nested(in_json, key_path)
        if value is None:
            continue
        set_nested(out_json, key_path, value)
    return out_json

def serialize_with_line_per_item(array: List[Json]) -> str:
    assert type(array) is list
    return '[' + '\n,'.join(json.dumps(obj) for obj in array) + '\n]\n'
