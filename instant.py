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





class DateTimeFormatter():

    _FORMAT_RE = re.compile('(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)')

    def __init__(self, locale='en_us'):

        self.locale = locales.get_locale(locale)

    def format(cls, dt, fmt):

        return cls._FORMAT_RE.sub(lambda m: cls._format_token(dt, m.group(0)), fmt)

    def _format_token(self, dt, token):

        if token == 'YYYY':
            return self.locale.year_full(dt.year)
        if token == 'YY':
            return self.locale.year_abbreviation(dt.year)

        if token == 'MMMM':
            return self.locale.month_name(dt.month)
        if token == 'MMM':
            return self.locale.month_abbreviation(dt.month)
        if token == 'MM':
            return '{0:02d}'.format(dt.month)
        if token == 'M':
            return str(dt.month)

        if token == 'DDDD':
            return '{0:03d}'.format(dt.timetuple().tm_yday)
        if token == 'DDD':
            return str(dt.timetuple().tm_yday)
        if token == 'DD':
            return '{0:02d}'.format(dt.day)
        if token == 'D':
            return str(dt.day)

        if token == 'Do':
            return self.locale.ordinal_number(dt.day)

        if token == 'dddd':
            return self.locale.day_name(dt.isoweekday())
        if token == 'ddd':
            return self.locale.day_abbreviation(dt.isoweekday())
        if token == 'd':
            return str(dt.isoweekday())

        if token == 'HH':
            return '{0:02d}'.format(dt.hour)
        if token == 'H':
            return str(dt.hour)
        if token == 'hh':
            return '{0:02d}'.format(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))
        if token == 'h':
            return str(dt.hour if 0 < dt.hour < 13 else abs(dt.hour - 12))

        if token == 'mm':
            return '{0:02d}'.format(dt.minute)
        if token == 'm':
            return str(dt.minute)

        if token == 'ss':
            return '{0:02d}'.format(dt.second)
        if token == 's':
            return str(dt.second)

        if token == 'SSSSSS':
            return str('{0:06d}'.format(int(dt.microsecond)))
        if token == 'SSSSS':
            return str('{0:05d}'.format(int(dt.microsecond / 10)))
        if token == 'SSSS':
            return str('{0:04d}'.format(int(dt.microsecond / 100)))
        if token == 'SSS':
            return str('{0:03d}'.format(int(dt.microsecond / 1000)))
        if token == 'SS':
            return str('{0:02d}'.format(int(dt.microsecond / 10000)))
        if token == 'S':
            return str(int(dt.microsecond / 100000))

        if token == 'X':
            return str(calendar.timegm(dt.utctimetuple()))

        if token in ['ZZ', 'Z']:
            separator = ':' if token == 'ZZ' else ''
            tz = dateutil_tz.tzutc() if dt.tzinfo is None else dt.tzinfo
            total_minutes = int(util.total_seconds(tz.utcoffset(dt)) / 60)

            sign = '+' if total_minutes > 0 else '-'
            total_minutes = abs(total_minutes)
            hour, minute = divmod(total_minutes, 60)

            return '{0}{1:02d}{2}{3:02d}'.format(sign, hour, separator, minute)

        if token in ('a', 'A'):
            return self.locale.meridian(dt.hour, token)
