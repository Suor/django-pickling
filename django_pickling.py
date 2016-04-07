VERSION = (0, 2)
__version__ = '.'.join(map(str, VERSION))


from django.db.models import Model
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

def model_unpickle(cls, data):
    obj = cls.__new__(cls)
    obj.__dict__.update(izip(attnames(cls), data))
    return obj
model_unpickle.__safe_for_unpickle__ = True

def Model__reduce__(self):
    if self._deferred:
        return original_Model__reduce__(self)
    else:
        cls = self.__class__
        data = self.__dict__.copy()

        vector = map(data.pop, attnames(cls))
        return (model_unpickle, (cls, vector), data)

if Model.__reduce__ != Model__reduce__:
    original_Model__reduce__ = Model.__reduce__
    Model.__reduce__ = Model__reduce__

