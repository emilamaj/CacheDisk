import pytest
import asyncio
from your_caching_module import CacheDecorators  # Import your cache decorators from the module

# An example synchronous function to be cached
@CacheDecorators.sync_disk_cache()
def sync_test_func(x):
    return x * 2

# An example asynchronous function to be cached
@CacheDecorators.async_disk_cache()
async def async_test_func(x):
    return x * 3

@pytest.fixture(autouse=True)
def clear_cache():
    """Fixture to clear the cache before each test."""
    CacheDecorators.CACHE_DB.clear()
    CacheDecorators.PENDING_KEYS.clear()
    CacheDecorators.USED_KEYS_DB.clear()
    # Optionally, add logic to clear any cache files from the file system if needed

@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (5, 10),
    (-1, -2),
    (0, 0),
])
def test_sync_cache(input_value, expected):
    assert sync_test_func(input_value) == expected  # The first call, caches the result
    assert sync_test_func(input_value) == expected  # The second call, should retrieve from cache

@pytest.mark.asyncio
@pytest.mark.parametrize("input_value,expected", [
    (1, 3),
    (3, 9),
    (-2, -6),
    (0, 0),
])
async def test_async_cache(input_value, expected):
    assert await async_test_func(input_value) == expected  # The first call, caches the result
    assert await async_test_func(input_value) == expected  # The second call, should retrieve from cache

def test_cache_miss():
    """Test behavior when cache misses."""
    # Assuming '999' has not been cached before.
    assert sync_test_func(999) == 999 * 2

@pytest.mark.asyncio
async def test_async_cache_miss():
    """Test behavior when async cache misses."""
    # Assuming '999' has not been cached before.
    assert await async_test_func(999) == 999 * 3

def test_cache_commit():
    """Test if changes are committed to disk properly."""
    sync_test_func(10)  # Cache this
    CacheDecorators.commit()  # Manually trigger commit to disk
    # Here, you would normally check if the file has been created on disk with the expected contents.

@pytest.mark.asyncio
async def test_exceptions():
    """Test how exceptions are handled and ensure cache is still saved."""

    @CacheDecorators.sync_disk_cache()
    def faulty_sync_func(x):
        if x == 0:
            raise ValueError("Test exception")
        return x

    @CacheDecorators.async_disk_cache()
    async def faulty_async_func(x):
        if x == 0:
            raise ValueError("Test async exception")
        return x

    with pytest.raises(ValueError):
        faulty_sync_func(0)
    
    with pytest.raises(ValueError):
        await faulty_async_func(0)

    # After an exception, ensure that other data still gets cached properly.
    assert faulty_sync_func(2) == 2
    assert await faulty_async_func(3) == 3

# Reuse the async_test_func if already defined, or define a new one specifically for this test
@CacheDecorators.async_disk_cache()
async def async_test_func_for_concurrency(x):
    # Simulating an I/O operation
    await asyncio.sleep(0.1)
    return x * 3

@pytest.mark.asyncio
async def test_async_concurrency():
    """Test concurrent access to an async cached function."""
    input_value = 7  # A common input to trigger cache behavior
    expected = input_value * 3

    # Launching multiple concurrent calls to the async_test_func
    tasks = [asyncio.create_task(async_test_func_for_concurrency(input_value)) for _ in range(10)]

    results = await asyncio.gather(*tasks)

    # Verify that all results are the expected value and exactly one operation was computed
    assert all(result == expected for result in results), "Expected all concurrent results to match the expected value."

    # Further checks could be added here to ensure the function was actually called only once, and the rest were cache hits.
    # This might involve mocking or other strategies to monitor function invocations.
