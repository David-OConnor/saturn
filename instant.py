import datetime as _datetime
from functools import partial
import re
from typing import TypeVar, Iterator

import pytz

# todo maybe make the funcs work on normal dt objects??

# No need to import datetime if using instant.
timedelta = _datetime.timedelta

class TzNaiveError(Exception):
    pass


# def datetime(*args, **kwargs):
def datetime(year: int, month: int, day: int, hour:int=0, minute:int=0,
        second:int=0, microsecond:int=0, tzinfo=None, tz=None):
    """Create a datetime instance, with default tzawareness at UTC."""

    dt = _datetime.datetime(year, month, day, hour, minute, second, microsecond,
        tzinfo)
    # dt = _datetime.datetime(*args, **kwargs)

    if tz:  # A string timezone is provided
        return fix_naive(dt, tz)
    elif dt.tzinfo:  # A timezone object is provided
        return dt
    else:  # No timezone provided; assume UTC.
        return dt.replace(tzinfo=pytz.utc)


def now() -> _datetime.datetime:
    """Similar to datetime.datetime.utcnow, but tz-aware."""
    # return from_datetime(datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
    return _datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


def fix_naive(dt: _datetime.datetime, tz: str='UTC') -> _datetime.datetime:
    """Convert a tz-naive datetime to tz-aware. Default to UTC"""
    return pytz.timezone(tz).localize(dt)


def _expand(dt: _datetime.datetime):
    """Expand arguments from a datetime object or instant."""
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, \
        dt.microsecond, dt.tzinfo


def to_iso(dt: _datetime.datetime) -> str:
    """Return a standard ISO 8601 datetime string.  Similar to datetime's
    .isoformat()"""
    # todo placeholder, not quite right.
    # return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}:{:02d}+{}".format(*_expand(dt))
    if not dt.tzinfo:
        raise TzNaiveError
    return dt.isoformat()


def to_str(dt: _datetime.datetime, format: str) -> str:
    """Format a datetime or Instant as a string."""
    if not dt.tzinfo:
        raise TzNaiveError

    # todo placeholder
    return dt.strftime(format)

    x = 1
    format_re = re.compile('(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)')

    pattern = re.compile('(YYYY)*|(YYYY)*|(MM)*|(DD)*')


def from_str(dt_str: str, format: str) -> _datetime.datetime:
    """Format a string to datetime.  Similar to datetime.strptime."""
    # todo placeholder
    dt = _datetime.datetime.strptime(dt_str, format)
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=pytz.utc)
    return dt


def move_tz(dt: _datetime.datetime, tz: str) -> _datetime.datetime:
    """Change a datetime from one timezone to another."""
    # Datetime provides a ValueError if you use this function on a naive DT, so
    # no need to explicitly raise an error here.
    return dt.astimezone(pytz.timezone(str))


def _count_timedelta(delta: _datetime.timedelta, step, seconds_in_interval: int) -> int:
    """Helper function for iterate.  Finds the number of intervals in the timedelta."""
    return int(delta.total_seconds() / (seconds_in_interval * step))


def range_dt(start, end, step=1, interval='day') -> Iterator[_datetime.datetime]:
    """Iterate over Instants or datetimes."""
    # todo deocorator to check for tz-naive?
    if not start.tzinfo or not end.tzinfo:
        raise TzNaiveError

    intervals = partial(_count_timedelta, (end - start), step)

    if interval == 'week':
        for i in range(intervals(3600 * 24 * 7)):
            yield start + _datetime.timedelta(weeks=i) * step

    elif interval == 'day':
        for i in range(intervals(3600 * 24)):
            yield start + _datetime.timedelta(days=i) * step

    elif interval == 'hour':
        for i in range(intervals(3600)):
            yield start + _datetime.timedelta(hours=i) * step

    elif interval == 'minute':
        for i in range(intervals(60)):
            yield start + _datetime.timedelta(minutes=i) * step

    elif interval == 'second':
        for i in range(intervals(1)):
            yield start + _datetime.timedelta(seconds=i) * step

    elif interval == 'millisecond':
        for i in range(intervals(1 / 1000)):
            yield start + _datetime.timedelta(milliseconds=i) * step

    elif interval == 'microsecond':
        for i in range(intervals(1 / 10e6)):
            yield start + _datetime.timedelta(microseconds=i) * step

    else:
        raise AttributeError("Interval must be 'week', 'day', 'hour' 'second', \
            'microsecond' or 'millisecond '")
