from setuptools import setup, find_packages

setup(
    name="CacheDisk",
    version="0.4",
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    # PyPI metadata
    author="Emile Amajar",
    description="A lightweight in-memory caching library with disk persistence. Supports both sync and async functions.",
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    keywords="cache caching disk cache-disk database key-value",
    url="https://github.com/emilamaj/CacheDisk",   # Project home page
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
