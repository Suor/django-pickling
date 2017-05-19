import pytest
try:
    import cPickle as pickle
except ImportError:
    import pickle

from .models import Post


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
@pytest.fixture(scope='session')
def post():
    return Post.objects.create(title='Pickling')


def test_equal(post):
    restored = pickle.loads(pickle.dumps(post, -1))
    assert restored == post


def test_packed(post):
    stored = pickle.dumps(post)
    assert b'model_unpickle' in stored  # Our unpickling function is used
    assert b'title' not in stored       # Attributes are packed
