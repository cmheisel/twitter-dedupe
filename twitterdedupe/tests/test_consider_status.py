import pytest


class MemoryCache(object):
    def __init__(self, preseed=None, prefix="memtest"):
        if preseed is None:
            preseed = {}
        self.prefix = prefix
        self._data = preseed

    def _key(self, key):
        return self.prefix + key

    def keys(self):
        return self._data.keys()

    def set(self, key, value, timeout=None):
        """Set key-value in cache with given timeout (or use default one)"""
        key = self._key(key)
        self._data[key] = value

    def get(self, key):
        """Get key-value from cache"""
        key = self._key(key)
        return self._data.get(key, None)

    def flush(self, pattern='', step=1000):
        self._data = {}


class Dummy(object):
    pass


class MockStatus(object):
    def __init__(self, screen_name, status_id, text, url=None):
        self.id = status_id,
        self.screen_name = screen_name
        self.entities = {
            'urls': []
        }
        self.text = text
        if url:
            self.entities['urls'].append({'expanded_url': url})

    @property
    def user(self):
        u = Dummy()
        u.screen_name = self.screen_name
        return u


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
def cache():
    return MemoryCache()


@pytest.fixture
def passthru_expand_fn():
    return lambda url: url


@pytest.fixture
def nonetwork_expand_fn():
    from test_lengthen_url import reqlib
    from twitterdedupe import lengthen_url

    def wrapped_lengthen_url(url):
        return lengthen_url(url, reqlib)
    return wrapped_lengthen_url


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
