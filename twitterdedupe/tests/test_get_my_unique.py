import pytest

from twitterdedupe.tests.helpers import (
    cache,
    MockStatus,
    MockAPI,
    nonetwork_expand_fn
)


@pytest.fixture
def meth():
    from twitterdedupe import get_my_unique_statuses
    return get_my_unique_statuses


@pytest.fixture
def one_unique_timeline():
    timeline = [
        MockStatus(
            "hitchhikers",
            44,
            "Most definitely not the question",
            "http://www.chrisheisel.com/?wpsrc=fol_tw"
        )
    ]
    return timeline

@pytest.fixture
def three_timeline():
    timeline = [
        MockStatus(
            "hitchhikers",
            44,
            "Most definitely not the question",
            "http://www.chrisheisel.com/?wpsrc=fol_tw"
        ),
        MockStatus(
            "hitchhikers",
            45,
            "Most definitely not the question but it is a dupe!",
            "http://www.chrisheisel.com/?wpsrc=fol_tw"
        ),
        MockStatus(
            "hitchhikers",
            46,
            "No links this time",
        ),
        MockStatus(
            "non-hitchhikers",
            3,
            "No links this time",
        )
    ]
    return timeline


def test_emtpy_timeline(meth, cache, nonetwork_expand_fn):
    api = MockAPI("cmheisel", [])
    result = meth(api, 1, cache, expand_fn=nonetwork_expand_fn)
    assert len(result) == 0


def test_one_unique_timeline(meth, cache,
                             nonetwork_expand_fn, one_unique_timeline):
    api = MockAPI("cmheisel", one_unique_timeline)
    result = meth(api, 1, cache, expand_fn=nonetwork_expand_fn)
    assert len(result) == 1


def test_three_timeline(meth, cache,
                             nonetwork_expand_fn, three_timeline):
    api = MockAPI("cmheisel", three_timeline)
    result = meth(api, 1, cache, expand_fn=nonetwork_expand_fn)
    assert len(result) == 3
