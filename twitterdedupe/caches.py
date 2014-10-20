class LocalCache(object):
    def __init__(self):
        self.data = {}

    def set(self, key, value, timeout=30):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)
