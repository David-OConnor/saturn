from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name = "Instant",
    version = "0.1",
    packages = find_packages(),

    install_requires = ['pytz>=2016.3'],

    author = "David O'Connor",
    author_email = "david.alan.oconnor@gmail.com",
    url = 'https://github.com/David-OConnor/instant',
    description = "Clean, easy datetime syntax; always tz-aware.",
    long_description = readme,
    license = "Apache",
    keywords = "datetime, pytz, timezone, tzinfo",
)
