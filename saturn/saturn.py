import datetime as _datetime
from functools import partial, wraps
from typing import TypeVar, Iterator

import pytz

from . import from_arrow


# No need to import datetime if using saturn.
timedelta = _datetime.timedelta
date = _datetime.date

DateOrDatetime = TypeVar('DateOrDatetime', _datetime.date, _datetime.datetime)
TimeOrDatetime = TypeVar('TimeOrDatetime', _datetime.time, _datetime.datetime)


class TzNaiveError(Exception):
    pass

# todo reorder func arguments to be curry-friendly? Needs toolz to support annotations, i guess


def _check_aware_input(func, num_dt_args=1):
    """Force a function that accepts a datetime as first argument to check for
    timezone-awareness.  Raise an error if the daatetime's naive."""
    @wraps(func)
    def inner(*args, **kwargs):
        dts = args[:num_dt_args]
        # Can't use isinstance, since isinstance([datetime object], _datetime.date)
        # returns True.
        for dt in dts:
            if type(dt) != _datetime.date:
                if not dt.tzinfo:
                    raise TzNaiveError("Must use a timezone-aware datetime. Consider saturn.fix_naive().")

        return func(*args, **kwargs)
    return inner


def _check_aware_output(func):
    """Check if a function's output is timezone-aware. Func's first output must
    be the dt; second must be a tz. Used  on functions where the result may, or
    may not be tz-aware already. If already, tz is ignored."""
    @wraps(func)
    def inner(*args, **kwargs):
        dt, tz = func(*args, **kwargs)
        if not dt.tzinfo:  # The time component might have a tzinfo.
            return fix_naive(dt, tz)
        return dt

    return inner


def _check_aware_input_2args(func):
    return _check_aware_input(func, num_dt_args=2)


def datetime(year: int, month: int, day: int, hour: int=0, minute: int=0,
             second: int=0, microsecond: int=0, tzinfo=None, tz=None) -> _datetime.datetime:
    """Create a datetime instance, with default tzawareness at UTC."""

    dt = _datetime.datetime(year, month, day, hour, minute, second,
                            microsecond, tzinfo)

    if tz:  # A string timezone is provided
        return fix_naive(dt, tz)
    elif dt.tzinfo:  # A timezone object is provided
        return dt
    else:  # No timezone provided; assume UTC.
        return dt.replace(tzinfo=pytz.utc)


def time(hour: int=0, minute: int=0, second: int=0,
         microsecond: int = 0, tzinfo=None, tz=None) -> _datetime.time:
    """Create a time instance, with default tzawareness at UTC."""

    t = _datetime.time(hour, minute, second, microsecond, tzinfo)

    if tz:  # A string timezone is provided
        return fix_naive(t, tz)
    elif t.tzinfo:  # A timezone object is provided
        return t
    else:  # No timezone provided; assume UTC.
        return t.replace(tzinfo=pytz.utc)


def now() -> _datetime.datetime:
    """Similar to datetime.datetime.utcnow, but tz-aware."""
    # return from_datetime(datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
    return _datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


@_check_aware_output
def combine(date_: _datetime.date, time_: _datetime.time, tz: str='UTC') -> _datetime.datetime:
    """Similar to datetime.datetime.combine, but tz-aware.  The optional
    tz argument won't override a tz included in the time component."""
    return _datetime.datetime.combine(date_, time_), tz


def fix_naive(dt: TimeOrDatetime, tz: str='UTC') -> _datetime.datetime:
    """Convert a tz-naive datetime to tz-aware. Default to UTC"""
    return pytz.timezone(tz).localize(dt)


def _expand(dt: TimeOrDatetime):
    """Expand arguments from a datetime object."""
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, \
        dt.microsecond, dt.tzinfo


@_check_aware_input
def to_str(dt: DateOrDatetime, str_format: str) -> str:
    """Format a datetime or date as a string."""
    return from_arrow.format_(dt, str_format)


@_check_aware_output
def from_str(dt_str: str, str_format: str, tz: str='UTC') -> _datetime.datetime:
    """Format a string to datetime.  Similar to datetime.strptime. The optional
    tz argument won't override a tz included in the string."""
    return from_arrow.parse(dt_str, str_format), tz


@_check_aware_input
def to_iso(dt: DateOrDatetime) -> str:
    """Return a standard ISO 8601 datetime string.  Similar to datetime's
    .isoformat()"""
    return dt.isoformat()


@_check_aware_output
def from_iso(iso_str: str, tz: str='UTC') -> _datetime.datetime:
    """Convert an ISO 8601 string to a datetime.  The optional
    tz argument won't override a tz included in the string."""
    return from_arrow.parse_iso(iso_str), tz
    #
    # if not dt.tzinfo:
    #     return dt.fix_naive(dt, tz)
    # return dt


def move_tz(dt: _datetime.datetime, tz: str) -> _datetime.datetime:
    """Change a datetime from one timezone to another."""
    # Datetime provides a ValueError if you use this function on a naive DT, so
    # no need to explicitly raise an error here.
    return dt.astimezone(pytz.timezone(tz))


def _count_timedelta(delta: _datetime.timedelta, step, seconds_in_interval: int) -> int:
    """Helper function for iterate.  Finds the number of intervals in the timedelta."""
    return int(delta.total_seconds() / (seconds_in_interval * step))


@_check_aware_input_2args
def range_dt(start: DateOrDatetime, end: DateOrDatetime, step: int=1,
             interval: str='day') -> Iterator[_datetime.datetime]:
    """Iterate over datetimes or dates, similar to builtin range.."""
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
        for i in range(intervals(1e-6)):
            yield start + _datetime.timedelta(microseconds=i) * step

    else:
        raise AttributeError("Interval must be 'week', 'day', 'hour' 'second', \
            'microsecond' or 'millisecond'.")
