"""
caches
From http://blog.seevl.fm/2013/11/22/simple-caching-with-redis/
"""

import cPickle


class RedisCache(object):
    """Redis cache"""

    def __init__(self, redis, prefix='cache|', timeout=60*60):
        """Create Redis cache instance using a StrictRedis connection,
        with prefix and timeout (or use default one)"""
        assert redis
        self._redis = redis
        self._prefix = prefix
        self._timeout = timeout

    def set(self, key, value, timeout=None):
        """Set key-value in cache with given timeout (or use default one)"""
        timeout = timeout or self._timeout
        key = self._prefix + key
        ## Add key and define an expire timeout in a pipeline for atomicity
        self._redis.pipeline().set(key, cPickle.dumps(value)).expire(key, timeout).execute()

    def get(self, key):
        """Get key-value from cache"""
        data = self._redis.get(self._prefix + key)
        return (data and cPickle.loads(data)) or None

    def flush(self, pattern='', step=1000):
        """Flush all cache (by group of step keys for efficiency),
        or only keys matching an optional pattern"""
        keys = self._redis.keys(self._prefix + pattern + '*')
        [self._redis.delete(*keys[i:i+step]) for i in xrange(0, len(keys), step)]
