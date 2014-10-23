import pytest

from twitterdedupe.tests.helpers import cache, MockStatus, nonetwork_expand_fn


@pytest.fixture
def meth():  # Crystal Blue Persuasion
    from twitterdedupe import consider_status
    return consider_status


@pytest.fixture
def text_status():
    status = MockStatus(
        "hitchhikers",
        42,
        "That's the question",
    )
    return status


@pytest.fixture
def link_status():
    status = MockStatus(
        "hitchhikers",
        43,
        "That's decidedly not the question",
        "http://www.chrisheisel.com/"
    )
    return status


@pytest.fixture
def repeat_link_status():
    status = MockStatus(
        "hitchhikers",
        44,
        "Most definitely not the question",
        "http://www.chrisheisel.com/"
    )
    return status


@pytest.fixture
def sneaky_link_status():
    status = MockStatus(
        "hitchhikers",
        44,
        "Most definitely not the question",
        "http://www.chrisheisel.com/?wpsrc=fol_tw"
    )
    return status


@pytest.fixture
def passthru_expand_fn():
    return lambda url: url


def test_new_text_tweet(meth, text_status, cache):
    result = meth(text_status, cache)
    assert result == text_status


def test_repeat_text_tweet(meth, text_status, cache):
    meth(text_status, cache)
    text_status.id = 999
    result = meth(text_status, cache)
    assert result is None


def test_new_link_tweet(meth, link_status, passthru_expand_fn, cache):
    result = meth(link_status, cache, expand_fn=passthru_expand_fn)
    assert result == link_status


def test_repeat_link_tweet(meth,
                           link_status,
                           repeat_link_status,
                           passthru_expand_fn,
                           cache):
    meth(link_status, cache, expand_fn=passthru_expand_fn)
    result = meth(repeat_link_status, cache, expand_fn=passthru_expand_fn)
    assert result is None


def test_sneaky_link_tweet(meth,
                           link_status,
                           sneaky_link_status,
                           nonetwork_expand_fn,
                           cache):
    meth(link_status, cache, expand_fn=nonetwork_expand_fn)
    result = meth(sneaky_link_status, cache, expand_fn=nonetwork_expand_fn)
    assert result is None
