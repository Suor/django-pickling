VERSION = (1, 0)
__version__ = '.'.join(map(str, VERSION))


from django.apps import apps
from django.conf import settings
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
        _cache[cls] = tuple(sorted(f.attname for f in cls._meta.fields))
        return _cache[cls]


def model_unpickle(model, vector, db, adding, _cache={}):
    try:
        cls = _cache[model]
    except KeyError:
        # Only needed in Django 1.8 and 1.9
        if not apps.ready:
            apps.populate(settings.INSTALLED_APPS)
        cls = _cache[model] = apps.get_model(*model.split('.'))
    obj = cls.__new__(cls)
    obj.__dict__.update(izip(attnames(cls), vector))

    # Restore state. This is the fastest way to create object I know.
    obj._state = ModelState.__new__(ModelState)
    obj._state.__dict__ = {'db': db, 'adding': adding}

    return obj
model_unpickle.__safe_for_unpickle__ = True


def Model__reduce__(self):
    cls = self.__class__
    opts = cls._meta
    # We do not pickle class but its identifier to work with dynamic models like m2m through ones
    # We use concat instead of tuple to spead up loads at an expense of dumps
    # This is the fastest way to concat here, formats are slower
    model = opts.app_label + '.' + opts.object_name
    data = self.__dict__.copy()
    state = data.pop('_state')
    try:
        # Popping all known attributes into vector, leaving the rest in data
        vector = tuple(data.pop(name) for name in attnames(cls))
        return (model_unpickle, (model, vector, state.db, state.adding), data)
    except KeyError:
        # data.pop() raises when some attnames are deferred
        return original_Model__reduce__(self)


if Model.__reduce__ != Model__reduce__:
    original_Model__reduce__ = Model.__reduce__
    Model.__reduce__ = Model__reduce__
    del Model.__setstate__  # Drop django version check
