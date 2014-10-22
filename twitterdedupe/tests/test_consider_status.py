import pytest


class MemoryCache(object):
    def __init__(self, preseed=None, prefix="memtest"):
        if preseed is None:
            preseed = {}
        self.prefix = prefix
        self._data = preseed

    def _key(self, key):
        return self.prefix + key

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
def cache():
    return MemoryCache()


def test_new_text_tweet(meth, text_status, cache):
    result = meth(text_status, cache)
    assert result == text_status


def test_repeat_text_tweet(meth, text_status, cache):
    meth(text_status, cache)
    text_status.id = 999
    result2 = meth(text_status, cache)
    assert result2 is None
