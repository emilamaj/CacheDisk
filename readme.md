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
result = expensive_function('some_input')

# Subsequent calls with the same input will fetch the result from the cache
cached_result = expensive_function('some_input')
```

For asynchronous functions, simply use the `@CacheDisk.async_disk_cache()` decorator in a similar fashion.

### Configuring the Cache Directory

By default, CacheDisk uses a directory named `cache_data` in your current working directory. You can customize the cache directory as follows:

```python
CacheDiskConfig.cache_dir = '/path/to/your/custom/cache/directory'
```

### Committing Cache Changes

To manually trigger saving all pending cache changes to disk:

```python
CacheDisk.commit()
```

This can be particularly useful before application shutdown or after a batch of operations.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have feedback, ideas, or code improvements.

## License

CacheDisk is licensed under the MIT License. See [LICENSE](LICENSE) file for more details.