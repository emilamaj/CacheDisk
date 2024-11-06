from setuptools import setup, find_packages

# Read version from __init__.py
with open('cachedisk/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"').strip("'")
            break

# Read README.md with error handling
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    try:
        with open('readme.md', 'r', encoding='utf-8') as f:
            long_description = f.read()
    except FileNotFoundError:
        long_description = """A lightweight in-memory caching library with disk persistence. 
        Supports both sync and async functions."""

setup(
    name="cachedisk",
    version=version,
    packages=find_packages(include=['cachedisk', 'cachedisk.*']),
    install_requires=[],
    python_requires='>=3.6',
    # PyPI metadata
    author="Emile Amajar",
    description="A lightweight in-memory caching library with disk persistence. Supports both sync and async functions.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="cache caching disk cache-disk database key-value",
    url="https://github.com/emilamaj/CacheDisk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
    license="MIT",
)
