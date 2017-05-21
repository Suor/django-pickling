VERSION = (0, 2)
__version__ = '.'.join(map(str, VERSION))


from django.db.models import Model
from django.db.models.base import ModelState
try:
    from itertools import izip
except ImportError:
    izip = zip


def attnames(cls, _cache={}):
    try:
        return _cache[cls]
    except KeyError:
        _cache[cls] = [f.attname for f in cls._meta.fields]
        return _cache[cls]


def model_unpickle(cls, vector, db, adding):
    obj = cls.__new__(cls)
    obj.__dict__.update(izip(attnames(cls), vector))

    # Restore state. This is the fastest way to create object I know.
    obj._state = ModelState.__new__(ModelState)
    obj._state.__dict__ = {'db': db, 'adding': adding}

    return obj
model_unpickle.__safe_for_unpickle__ = True


def Model__reduce__(self):
    cls = self.__class__
    data = self.__dict__.copy()
    state = data.pop('_state')
    try:
        vector = tuple(data.pop(name) for name in attnames(cls))
        return (model_unpickle, (cls, vector, state.db, state.adding), data)
    except KeyError:
        # data.pop() raises when some attnames are deferred
        return original_Model__reduce__(self)


if Model.__reduce__ != Model__reduce__:
    original_Model__reduce__ = Model.__reduce__
    Model.__reduce__ = Model__reduce__
    del Model.__setstate__  # Drop django version check
