import pytest
pytestmark = pytest.mark.django_db

from .test_db import pickle, post


def bench_dumps(benchmark, post):
    benchmark(pickle.dumps, post, -1)


def bench_loads(benchmark, post):
    stored = pickle.dumps(post, -1)
    benchmark(pickle.loads, stored)
