# CacheDisk

CacheDisk is a lightweight, in-memory caching library designed for Python, offering seamless disk persistence.
It provides a drop-in optimization for your frequently used sync/async functions, allowing you to cache their results and retrieve them from memory on subsequent calls.

## Features

- Easy-to-use decorators to cache the results of functions, both synchronously and asynchronously.
- Disk persistence allows your cache to survive across application restarts, enhancing data retrieval times for repeated operations.
- Flexible storage options with support for JSON and Pickle, choose according to your compatibility or performance needs.
- Culling functionality to remove infrequently used cache entries, ensuring that your cache does not grow unbounded.
- Configurable caching parameters allowing fine-tuned performance to match the needs of your application, by avoiding slow-downs caused by disk writes.

## Installation

CacheDisk is available on PyPi and can be installed using pip:

```bash
pip install cachedisk
```

## Quick Start

### Basic Caching Example

Here's a quick example to get you started with CacheDisk:

```python
from cachedisk import CacheDisk, CacheDiskConfig

# Optional: Configure CacheDisk to use JSON for serialization
CacheDiskConfig.use_json = True

@CacheDisk.sync_disk_cache()
def expensive_function(param1):
    # Simulate an expensive or time-consuming operation
    return some_expensive_computation(param1)

# First call will compute and cache the result
result = expensive_function('some_input') # Takes 10 seconds to return

# Subsequent calls with the same input will fetch the result from the cache
cached_result = expensive_function('some_input') # Returns in 0ms
```

For asynchronous functions, simply use the `@CacheDisk.async_disk_cache()` decorator in a similar fashion:

```python
@CacheDisk.async_disk_cache()
async def expensive_function(param1):
    return some_expensive_computation(param1)
```

### Advanced Usage

You can customize the behavior of the cache by passing additional parameters to the decorators:

- `factor`: The factor which determines when should the save to disk operation be force-triggered. A factor of 0.33  (default value) means that the cache will be saved to disk every 33% of the cache size changes.
- `delay`: The delay in seconds after which the save to disk operation will be force-triggered if there are no save operations due to cache size changes.
- `cache_none`: Whether to cache the result of the function when it returns None. This can be useful if you want to recompute the result of the function when it returns None (possibly due to exceptions).

Here's an example:
```python
@CacheDisk.async_disk_cache(factor=0.50, delay=120, cache_none=False)
async def expensive_function(param1):
    return some_expensive_computation(param1)
```

### Configuring the Cache Directory

By default, CacheDisk uses a directory named `cache_data` in your current working directory. You can customize the cache directory as follows:

```python
CacheDiskConfig.cache_dir = '/path/to/your/custom/cache/directory'
```

### Caveat:Committing Cache Changes

Some pending cache changes may not be saved to disk if the program is terminated abruptly right after the cache is updated but before the changes are written to disk.
To manually trigger saving all pending cache changes to disk:

```python
CacheDisk.commit()
```

This can be particularly useful before application shutdown or after a batch of operations.
This delayed commit behavior is put in place to avoid degrading the SSD/HDD longevity with frequent writes.
It can however be completely disabled by passing the parameter

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have feedback, ideas, or code improvements.

## License

CacheDisk is licensed under the MIT License. See [LICENSE](LICENSE) file for more details.