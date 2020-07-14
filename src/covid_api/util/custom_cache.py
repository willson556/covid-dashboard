import threading
from time import time
from flask_caching.backends import UWSGICache

class UWSGIFastCache(UWSGICache):
    """A Cache that can greatly improve large object cache performance at the expense of memory usage."""
    class ThreadLocalDictionary(threading.local):
        def __init__(self):
            self.storage = {}

    def __init__(self, default_timeout=300, cache=""):
        super().__init__(default_timeout, cache)
        self._memory_cache = self.ThreadLocalDictionary()

    def _get_cache(self):
        return self._memory_cache.storage

    def _set(self, key, value, timeout):
        expires = self._normalize_timeout(timeout)
        self._get_cache()[key] = (value, expires)

    def set(self, key, value, timeout=None):
        self._set(key, value, timeout)
        super().set(key, (value, timeout), timeout)
    
    def get(self, key):
        in_uwsgi = self.has(key)

        if key in self._get_cache():
            value, expires = self._get_cache()[key]

            if not in_uwsgi or (expires != 0 and expires > time()):
                del self._get_cache()[key]
            else:
                return value
        
        if in_uwsgi:
            value, timeout = super().get(key)
            self._set(key, value, timeout)
            return value
        else:
            return None
    
    def add(self, key, value, timeout=None):
        if super().add(key, (value, timeout), timeout):
            self._set(key, value, timeout)
            return True
        
        return False

    def clear(self):
        self._memory_cache = self.ThreadLocalDictionary()
        super().clear()

def uwsgi_fast(app, config, args, kwargs):
    return UWSGIFastCache(*args, **kwargs)