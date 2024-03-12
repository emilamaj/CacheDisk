"""
A module to easily cache sync/async functions to memory or disk.
Includes decorators for caching functionality, supporting both synchronous and asynchronous calls.
The cache can be configured to use either JSON or Pickle format for disk storage.
The cache can be pruned to remove infrequently used keys.
"""

import os
import json
import pickle
import time
from functools import wraps

class CacheDiskConfig:
    """Configuration settings for the cache."""
    cache_dir = 'cache_data'
    use_json = False

class CacheDiskFileManager:
    """Handles the file operations for caching, including loading and saving caches."""

    @staticmethod
    def get_cache_filename(func_name):
        """Generates a filename based on the function name."""
        return os.path.join(CacheDiskConfig.cache_dir, f"{func_name}_cache.bak")

    @classmethod
    def load_cache(cls, func_name):
        """Loads the cache from the disk."""
        print(f"Loading cache for {func_name}...")
        filename = cls.get_cache_filename(func_name)
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    return json.load(f) if CacheDiskConfig.use_json else pickle.load(f)
            except (json.JSONDecodeError, pickle.UnpicklingError) as e:
                print(f"Error loading cache for {func_name}: {e}")
        return {}

    @classmethod
    def save_cache(cls, func_name, cache):
        """Saves the cache to the disk."""
        filename = cls.get_cache_filename(func_name)
        filename_temp = filename + '.temp'
        try:
            os.makedirs(CacheDiskConfig.cache_dir, exist_ok=True)
            with open(filename_temp, 'wb') as f:
                json.dump(cache, f) if CacheDiskConfig.use_json else pickle.dump(cache, f)
            os.replace(filename_temp, filename)
        except IOError as e:
            print(f"Error saving cache for {func_name}: {e}")

class CacheDisk:
    """Contains decorators for caching function results, with support for database culling."""

    CACHE_DB = {}
    PENDING_KEYS = set()
    USED_KEYS_DB = {}

    @staticmethod
    def is_null_result(result):
        """Checks if the result is None or contains only None values."""
        if result is None:
            return True
        elif isinstance(result, (list, tuple)):
            return all(x is None for x in result)
        return False

    @classmethod
    def commit(cls):
        """Saves all pending changes to the disk."""
        for func_name, cache in cls.CACHE_DB.items():
            if func_name in cls.PENDING_KEYS:
                CacheDiskFileManager.save_cache(func_name, cache)
                cls.PENDING_KEYS.remove(func_name)

    @classmethod
    def sync_disk_cache(cls, factor=0.33, delay=120, cache_none=False):
        """Decorator for caching sync functions to the disk."""
        def decorator(func):
            cache = CacheDiskFileManager.load_cache(func.__name__)
            cls.CACHE_DB[func.__name__] = cache
            last_len = len(cache)
            last_write = time.time()

            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal last_len, last_write
                key = args
                if key in cache:
                    result = cache[key]
                    if not cls.is_null_result(result) or cache_none:
                        return result

                try:
                    result = func(*args, **kwargs)
                    cache[key] = result
                    if cls.is_null_result(result):
                        print(f"Cacher: Null result for {func.__name__}({args})")

                    if len(cache) > last_len * (1 + factor) or time.time() - last_write > delay:
                        CacheDiskFileManager.save_cache(func.__name__, cache)
                        last_len = len(cache)
                        last_write = time.time()
                        cls.PENDING_KEYS.discard(func.__name__)
                    else:
                        cls.PENDING_KEYS.add(func.__name__)

                    # Keep track of used keys for culling
                    if func.__name__ not in cls.USED_KEYS_DB:
                        cls.USED_KEYS_DB[func.__name__] = set()
                    cls.USED_KEYS_DB[func.__name__].add(key)

                except (KeyboardInterrupt, SystemExit):
                    result = None
                    cls.commit()
                    raise

                return result
            return wrapper
        return decorator

    @classmethod
    def async_disk_cache(cls, factor=0.33, delay=120, cache_none=False):
        """
        Decorator for caching async functions to the disk.
        It mirrors the behavior of the sync_disk_cache decorator, adapted for asynchronous functions.
        """
        def decorator(func):
            cache = CacheDiskFileManager.load_cache(func.__name__)
            cls.CACHE_DB[func.__name__] = cache
            last_len = len(cache)
            last_write = time.time()

            @wraps(func)
            async def wrapper(*args, **kwargs):
                nonlocal last_len, last_write
                key = args

                if key in cache:
                    result = cache[key]
                    if not cls.is_null_result(result) or cache_none:
                        return result

                try:
                    # The only change from the sync decorator is the await keyword here.
                    result = await func(*args, **kwargs)
                    cache[key] = result
                    if cls.is_null_result(result):
                        print(f"Cacher: Null result for {func.__name__}({args})")

                    if len(cache) > last_len * (1 + factor) or time.time() - last_write > delay:
                        CacheDiskFileManager.save_cache(func.__name__, cache)
                        last_len = len(cache)
                        last_write = time.time()
                        cls.PENDING_KEYS.discard(func.__name__)
                    else:
                        cls.PENDING_KEYS.add(func.__name__)

                    # Keep track of used keys for culling
                    if func.__name__ not in cls.USED_KEYS_DB:
                        cls.USED_KEYS_DB[func.__name__] = set()
                    cls.USED_KEYS_DB[func.__name__].add(key)

                except (KeyboardInterrupt, SystemExit):
                    result = None
                    cls.commit()
                    raise

                return result
            return wrapper
        return decorator

    @classmethod
    def cull_db(cls, threshold=1):
        """Removes entries that are less frequently used than the specified threshold."""
        for func_name, used_keys in cls.USED_KEYS_DB.items():
            infrequently_used_keys = {key for key in cls.CACHE_DB[func_name] if key not in used_keys or used_keys[key] < threshold}
            for key in infrequently_used_keys:
                del cls.CACHE_DB[func_name][key]
            if not cls.CACHE_DB[func_name]:
                del cls.CACHE_DB[func_name]  # Remove the function entry if it has no keys
            else:
                CacheDiskFileManager.save_cache(func_name, cls.CACHE_DB[func_name])  # Save remaining keys to the disk
            cls.USED_KEYS_DB[func_name] = {k: v for k, v in used_keys.items() if v >= threshold}
