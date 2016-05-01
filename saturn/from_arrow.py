# This module includes code taken from crsmith's Arrow package, for string formatting.
# Arrow is © Copyright 2013, Chris Smith, licensed under Apache 2.
# Arrow on pypi: https://pypi.python.org/pypi/arrow
# Arrow homepage and documentation: http://arrow.readthedocs.io/en/latest/
# Arrow in Github: https://github.com/crsmithdev/arrow

import calendar
import re

import pytz


def format(dt, str_format):
    locale = EnglishLocale()
    _FORMAT_RE = re.compile(
        '(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)')

    return _FORMAT_RE.sub(lambda m: format_token(dt, m.group(0), locale),
                          str_format)


class Locale(object):
    """Represents locale-specific data and functionality."""

    names = []

    timeframes = {
        'now': '',
        'seconds': '',
        'minute': '',
        'minutes': '',
        'hour': '',
        'hours': '',
        'day': '',
        'days': '',
        'month': '',
        'months': '',
        'year': '',
        'years': '',
    }

    meridians = {
        'am': '',
        'pm': '',
        'AM': '',
        'PM': '',
    }

    past = None
    future = None

    month_names = []
    month_abbreviations = []

    day_names = []
    day_abbreviations = []

    ordinal_day_re = r'(\d+)'

    def __init__(self):

        self._month_name_to_ordinal = None

    def describe(self, timeframe, delta=0, only_distance=False):
        """ Describes a delta within a timeframe in plain language.
        :param timeframe: a string representing a timeframe.
        :param delta: a quantity representing a delta in a timeframe.
        :param only_distance: return only distance eg: "11 seconds" without "in" or "ago" keywords
        """

        humanized = self._format_timeframe(timeframe, delta)
        if not only_distance:
            humanized = self._format_relative(humanized, timeframe, delta)

        return humanized

    def day_name(self, day):
        """ Returns the day name for a specified day of the week.
        :param day: the ``int`` day of the week (1-7).
        """

        return self.day_names[day]

    def day_abbreviation(self, day):
        """ Returns the day abbreviation for a specified day of the week.
        :param day: the ``int`` day of the week (1-7).
        """

        return self.day_abbreviations[day]

    def month_name(self, month):
        """ Returns the month name for a specified month of the year.
        :param month: the ``int`` month of the year (1-12).
        """

        return self.month_names[month]

    def month_abbreviation(self, month):
        """ Returns the month abbreviation for a specified month of the year.
        :param month: the ``int`` month of the year (1-12).
        """

        return self.month_abbreviations[month]

    def month_number(self, name):
        """ Returns the month number for a month specified by name or abbreviation.
        :param name: the month name or abbreviation.
        """

        if self._month_name_to_ordinal is None:
            self._month_name_to_ordinal = self._name_to_ordinal(self.month_names)
            self._month_name_to_ordinal.update(self._name_to_ordinal(self.month_abbreviations))

        return self._month_name_to_ordinal.get(name)

    def year_full(self, year):
        """  Returns the year for specific locale if available
        :param name: the ``int`` year (4-digit)
        """
        return '{0:04d}'.format(year)

    def year_abbreviation(self, year):
        """ Returns the year for specific locale if available
        :param name: the ``int`` year (4-digit)
        """
        return '{0:04d}'.format(year)[2:]

    def meridian(self, hour, token):
        """ Returns the meridian indicator for a specified hour and format token.
        :param hour: the ``int`` hour of the day.
        :param token: the format token.
        """

        if token == 'a':
            return self.meridians['am'] if hour < 12 else self.meridians['pm']
        if token == 'A':
            return self.meridians['AM'] if hour < 12 else self.meridians['PM']

    def ordinal_number(self, n):
        """ Returns the ordinal format of a given integer
        :param n: an integer
        """
        return self._ordinal_number(n)

    def _ordinal_number(self, n):
        return '{0}'.format(n)

    def _name_to_ordinal(self, lst):
        return dict(map(lambda i: (i[1].lower(), i[0] + 1), enumerate(lst[1:])))

    def _format_timeframe(self, timeframe, delta):

        return self.timeframes[timeframe].format(abs(delta))

    def _format_relative(self, humanized, timeframe, delta):

        if timeframe == 'now':
            return humanized

        direction = self.past if delta < 0 else self.future

        return direction.format(humanized)




class EnglishLocale(Locale):

    names = ['en', 'en_us', 'en_gb', 'en_au', 'en_be', 'en_jp', 'en_za', 'en_ca']

    past = '{0} ago'
    future = 'in {0}'

    timeframes = {
        'now': 'just now',
        'seconds': 'seconds',
        'minute': 'a minute',
        'minutes': '{0} minutes',
        'hour': 'an hour',
        'hours': '{0} hours',
        'day': 'a day',
        'days': '{0} days',
        'month': 'a month',
        'months': '{0} months',
        'year': 'a year',
        'years': '{0} years',
    }

    meridians = {
        'am': 'am',
        'pm': 'pm',
        'AM': 'AM',
        'PM': 'PM',
    }

    month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']
    month_abbreviations = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']

    day_names = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_abbreviations = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    ordinal_day_re = r'((?P<value>[2-3]?1(?=st)|[2-3]?2(?=nd)|[2-3]?3(?=rd)|[1-3]?[04-9](?=th)|1[1-3](?=th))(st|nd|rd|th))'

    def _ordinal_number(self, n):
        if n % 100 not in (11, 12, 13):
            remainder = abs(n) % 10
            if remainder == 1:
                return '{0}st'.format(n)
            elif remainder == 2:
                return '{0}nd'.format(n)
            elif remainder == 3:
                return '{0}rd'.format(n)
        return '{0}th'.format(n)


def format_token(dt, token, locale):
    if token == 'YYYY':
        return locale.year_full(dt.year)
    if token == 'YY':
        return locale.year_abbreviation(dt.year)

    if token == 'MMMM':
        return locale.month_name(dt.month)
    if token == 'MMM':
        return locale.month_abbreviation(dt.month)
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
        return locale.ordinal_number(dt.day)

    if token == 'dddd':
        return locale.day_name(dt.isoweekday())
    if token == 'ddd':
        return locale.day_abbreviation(dt.isoweekday())
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
        tz = pytz.utc if dt.tzinfo is None else dt.tzinfo
        total_minutes = int(tz.utcoffset(dt).total_seconds() / 60)

        sign = '+' if total_minutes > 0 else '-'
        total_minutes = abs(total_minutes)
        hour, minute = divmod(total_minutes, 60)

        return '{0}{1:02d}{2}{3:02d}'.format(sign, hour, separator, minute)

    if token in ('a', 'A'):
        return locale.meridian(dt.hour, token)
