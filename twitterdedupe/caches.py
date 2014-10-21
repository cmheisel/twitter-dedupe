class LocalCache(object):
    def __init__(self):
        self.data = {}

    def set(self, key, value, timeout=30):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)


class RedisCache(object):
    def __init__(self, redis, timeout=30):
        self.redis = redis
        self.timeout = timeout

    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.timeout
        self.redis.setex(key, timeout, value)

    def get(self, key, default=None):
        result = self.redis.get(key)
        if result is None:
            return default
