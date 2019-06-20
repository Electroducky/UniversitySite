import json
from enum import Enum


class Wrapper(dict):
    __getattr__ = dict.__getitem__

    def __setattr__(self, key, value):
        if key != 'doc_id':
            dict.__setitem__(self, key, value)
        else:
            super.__setattr__(self, key, value)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return other._asdict().items() == dict.items(self)
        return dict.items(self) == other.__dict__.items()


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__ if not isinstance(o, Enum) else str(o)))


def to_object(document):
    if document is None:
        return None
    loaded_obj = json.loads(json.dumps(document), object_hook=lambda d: Wrapper(d))
    loaded_obj.doc_id = document.doc_id
    return loaded_obj