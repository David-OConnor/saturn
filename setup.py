from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name = "Instant",
    version = "0.1",
    packages = find_packages(),

    install_requires = ['pytz>=2016.3],

    author = "David O'Connor",
    author_email = "david.alan.oconnor@gmail.com",
    url = 'https://github.com/David-OConnor/instant',
    description = "Thin wrapper on datetime, with improvements.",
    long_description = readme,
    license = "Apache",
    keywords = "fast, numba, math, numerical, optimized, compiled",
)
