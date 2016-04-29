import datetime
from functools import partial
import re
from typing import TypeVar, Iterator

import pytz

# todo maybe make the funcs work on normal dt objects??

# No need to import datetime if using instant.
timedelta = datetime.timedelta

class TzNaiveError(Exception):
    pass


class Instant:
    def __init__(self, year: int, month: int, day: int, hour:int=0, minute:int=0,
            second:int=0, microsecond:int=0, tzinfo=pytz.utc):
        # Boilerplate
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self.tzinfo = tzinfo

        self.datetime = datetime.datetime(year, month, day, hour, minute,
            second, microsecond, tzinfo)


        def __add__(self, other):
            return self.datetime + other

        def __repr__(self):
            # return to_iso(self)
            return self.datetime.isoformat()

        @staticmethod
        def from_datetime(self, dt: datetime.datetime):
            return from_datetime(dt)

        @staticmethod
        def format(format_str: str):
            return format(format_str)


def Instant2(*args, **kwargs):
    """Create a datetime instance, with default tzawareness at UTC."""
    dt = datetime.datetime(*args, **kwargs)

    if dt.tzinfo:
        return dt
    else:
        return dt.replace(tzinfo=pytz.utc)


moment = TypeVar('Moment', datetime.datetime, Instant)


def from_datetime(dt: datetime.datetime) -> Instant:
    """Convert a datetime.datetime object to an Instant."""
    return Instant(*_expand(dt))


def to_datetime(inst: Instant) -> datetime.datetime:
    """Convert a datetime.datetime object to an Instant."""
    return datetime.datetime(*_expand(inst))


def now() -> datetime.datetime:
    """Similar to datetime.datetime.utcnow, but tz-aware."""
    # return from_datetime(datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


def fix_naive(dt: datetime.datetime) -> datetime.datetime:
    """Convert a tz-naive datetime to tz-aware @ UTC."""
    return dt.replace(tzinfo=pytz.utc)


def _expand(dt: moment):
    """Expand arguments from a datetime object or instant."""
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, \
        dt.microsecond, dt.tzinfo


def to_iso(dt: moment) -> str:
    """Return a standard ISO 8601 datetime string.  Similar to datetime's
    .isoformat()"""
    # todo placeholder, not quite right.
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}:{:02d}+{}".format(*_expand(dt))


def to_str(dt: moment, format: str) -> str:
    """Format a datetime or Instant as a string."""
    if not dt.tzinfo:
        raise TzNaiveError

    # todo placeholder
    return dt.strftime(format)

    x = 1
    format_re = re.compile('(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)')

    pattern = re.compile('(YYYY)*|(YYYY)*|(MM)*|(DD)*')


def from_str(dt_str: str, format: str) -> Instant:
    """Format a string to datetime.  Similar to datetime.strptime."""
    # todo placeholder
    dt = datetime.datetime.strptime(dt_str, format)
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=pytz.utc)
    return dt


def _count_timedelta(delta: datetime.timedelta, seconds_in_interval: int) -> int:
    """Helper function for iterate.  Finds the number of intervals in the timedelta."""
    return int(delta.total_seconds() / (seconds_in_interval))


def iterate(start, end, interval='day') -> Iterator[Instant]:
    """Iterate over Instants or datetimes."""
    # todo deocorator to check for tz-naive?
    if not start.tzinfo or not end.tzinfo:
        raise TzNaiveError

    intervals = partial(_count_timedelta, (end - start))

    if interval == 'week':
        for i in range(intervals(3600 * 24 * 7)):
            yield start + datetime.timedelta(weeks=i)

    elif interval == 'day':
        for i in range(intervals(3600 * 24)):
            yield start + datetime.timedelta(days=i)

    elif interval == 'hour':
        for i in range(intervals(3600)):
            yield start + datetime.timedelta(hours=i)

    elif interval == 'minute':
        for i in range(intervals(60)):
            yield start + datetime.timedelta(minutes=i)

    elif interval == 'second':
        for i in range(intervals(1)):
            yield start + datetime.timedelta(seconds=i)

    elif interval == 'millisecond':
        for i in range(intervals(1 / 1000)):
            yield start + datetime.timedelta(milliseconds=i)

    elif interval == 'microsecond':
        for i in range(intervals(1 / 10e6)):
            yield start + datetime.timedelta(microseconds=i)

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
