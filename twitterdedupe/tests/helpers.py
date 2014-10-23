import pytest


@pytest.fixture
def nonetwork_expand_fn():
    from test_lengthen_url import reqlib
    from twitterdedupe import lengthen_url

    def wrapped_lengthen_url(url):
        return lengthen_url(url, reqlib)
    return wrapped_lengthen_url


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


@pytest.fixture
def cache():
    return MemoryCache()


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


class MockAPI(object):
    def __init__(self, screen_name, home_timeline=None):
        if home_timeline is None:
            home_timeline = []
        self.screen_name = screen_name
        self._home_timeline = home_timeline

    def me(self):
        u = Dummy()
        u.screen_name = self.screen_name
        return u

    def home_timeline(self, *args, **kwargs):
        return self._home_timeline
