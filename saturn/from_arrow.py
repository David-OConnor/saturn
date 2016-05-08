# This module is modified code from crsmith's Arrow package, for string formatting.
# Arrow is © Copyright 2013, Chris Smith, licensed under Apache 2.
# Arrow on pypi: https://pypi.python.org/pypi/arrow
# Arrow homepage and documentation: http://arrow.readthedocs.io/en/latest/
# Arrow in Github: https://github.com/crsmithdev/arrow

import calendar
import datetime
import re

import pytz


RES = {
    'format': re.compile('(YYY?Y?|MM?M?M?|Do|DD?D?D?|d?dd?d?|HH?|hh?|mm?|ss?|SS?S?S?S?S?|ZZ?|a|A|X)'),
    'escape': re.compile('\[[^\[\]]*\]'),
    'one_through_six': re.compile('\d{1,6}'),
    'one_through_five': re.compile('\d{1,5}'),
    'one_through_four': re.compile('\d{1,4}'),
    'one_two_or_three': re.compile('\d{1,3}'),
    'one_or_two': re.compile('\d{1,2}'),
    'four_digit': re.compile('\d{4}'),
    'two_digit': re.compile('\d{2}'),
    'tz': re.compile('[+\-]?\d{2}:?(\d{2})?'),
    'tz_name': re.compile('\w[\w+\-/]+'),
    'tzinfo': re.compile('([+\-])?(\d\d):?(\d\d)?'),
}


BASE_INPUT_RE_MAP = {
    'YYYY': RES['four_digit'],
    'YY': RES['two_digit'],
    'MM': RES['two_digit'],
    'M': RES['one_or_two'],
    'DD': RES['two_digit'],
    'D': RES['one_or_two'],
    'HH': RES['two_digit'],
    'H': RES['one_or_two'],
    'hh': RES['two_digit'],
    'h': RES['one_or_two'],
    'mm': RES['two_digit'],
    'm': RES['one_or_two'],
    'ss': RES['two_digit'],
    's': RES['one_or_two'],
    'X': re.compile('\d+'),
    'ZZZ': RES['tz_name'],
    'ZZ': RES['tz'],
    'Z': RES['tz'],
    'SSSSSS': RES['one_through_six'],
    'SSSSS': RES['one_through_five'],
    'SSSS': RES['one_through_four'],
    'SSS': RES['one_two_or_three'],
    'SS': RES['one_or_two'],
    'S': re.compile('\d'),
}

MARKERS = ['YYYY', 'MM', 'DD']
SEPARATORS = ['-', '/', '.']


class ParserError(RuntimeError):
    pass


def format_(dt, str_format):
    locale = EnglishLocale()
    return RES['format'].sub(lambda m: format_token(dt, m.group(0), locale),
                             str_format)


class Locale:
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
        """ Returns the meridian indicator for a specified hour and format_ token.
        :param hour: the ``int`` hour of the day.
        :param token: the format_ token.
        """

        if token == 'a':
            return self.meridians['am'] if hour < 12 else self.meridians['pm']
        if token == 'A':
            return self.meridians['AM'] if hour < 12 else self.meridians['PM']

    def ordinal_number(self, n):
        """ Returns the ordinal format_ of a given integer
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

    @staticmethod
    def _ordinal_number(n):
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
        return locale._ordinal_number(dt.day)

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


def choice_re(choices, flags=0):
    """Helper function for parse."""
    return re.compile('({0})'.format('|'.join(choices)), flags=flags)


def parse_iso(iso_str):
    has_time = 'T' in iso_str or ' ' in iso_str.strip()
    space_divider = ' ' in iso_str.strip()

    if has_time:
        if space_divider:
            date_string, time_string = iso_str.split(' ', 1)
        else:
            date_string, time_string = iso_str.split('T', 1)
        time_parts = re.split('[+-]', time_string, 1)
        has_tz = len(time_parts) > 1
        has_seconds = time_parts[0].count(':') > 1
        has_subseconds = '.' in time_parts[0]

        if has_subseconds:
            subseconds_token = 'S' * min(len(re.split('\D+', time_parts[0].split('.')[1], 1)[0]), 6)
            formats = ['YYYY-MM-DDTHH:mm:ss.%s' % subseconds_token]
        elif has_seconds:
            formats = ['YYYY-MM-DDTHH:mm:ss']
        else:
            formats = ['YYYY-MM-DDTHH:mm']
    else:
        has_tz = False
        # generate required formats: YYYY-MM-DD, YYYY-MM-DD, YYYY
        # using various separators: -, /, .
        l = len(MARKERS)
        formats = [separator.join(MARKERS[:l-i])
                   for i in range(l)
                   for separator in SEPARATORS]

    if has_time and has_tz:
        formats = [f + 'Z' for f in formats]

    if space_divider:
        formats = [item.replace('T', ' ', 1) for item in formats]

    return parse_multiformat(iso_str, formats)


def parse(string, fmt):
    if isinstance(fmt, list):
        return parse_multiformat(string, fmt)

    locale = EnglishLocale()

    # fmt is a string of tokens like 'YYYY-MM-DD'
    # we construct a new string by replacing each
    # token by its pattern:
    # 'YYYY-MM-DD' -> '(?P<YYYY>\d{4})-(?P<MM>\d{2})-(?P<DD>\d{2})'
    tokens = []
    offset = 0

    input_re_map = BASE_INPUT_RE_MAP.copy()
    input_re_map.update({
        'MMMM': choice_re(locale.month_names[1:], re.IGNORECASE),
        'MMM': choice_re(locale.month_abbreviations[1:],
                         re.IGNORECASE),
        'Do': re.compile(locale.ordinal_day_re),
        'dddd': choice_re(locale.day_names[1:], re.IGNORECASE),
        'ddd': choice_re(locale.day_abbreviations[1:],
                         re.IGNORECASE),
        'd': re.compile("[1-7]"),
        'a': choice_re(
            (locale.meridians['am'], locale.meridians['pm'])
        ),
        # note: 'A' token accepts both 'am/pm' and 'AM/PM' formats to
        # ensure backwards compatibility of this token
        'A': choice_re(locale.meridians.values())
    })

    # Extract the bracketed expressions to be reinserted later.
    escaped_fmt = re.sub(RES['escape'], "#" , fmt)
    escaped_data = re.findall(RES['escape'], fmt)

    fmt_pattern = escaped_fmt

    for m in RES['format'].finditer(escaped_fmt):
        token = m.group(0)
        try:
            input_re = input_re_map[token]
        except KeyError:
            raise ParserError('Unrecognized token \'{0}\''.format(token))
        input_pattern = '(?P<{0}>{1})'.format(token, input_re.pattern)
        tokens.append(token)
        # a pattern doesn't have the same length as the token
        # it replaces! We keep the difference in the offset variable.
        # This works because the string is scanned left-to-right and matches
        # are returned in the order found by finditer.
        fmt_pattern = fmt_pattern[:m.start() + offset] + input_pattern + fmt_pattern[m.end() + offset:]
        offset += len(input_pattern) - (m.end() - m.start())

    final_fmt_pattern = ""
    a = fmt_pattern.split("#")
    b = escaped_data

    # Due to the way Python splits, 'a' will always be longer
    for i in range(len(a)):
        final_fmt_pattern += a[i]
        if i < len(b):
            final_fmt_pattern += b[i][1:-1]

    match = re.search(final_fmt_pattern, string, flags=re.IGNORECASE)
    if match is None:
        raise ParserError('Failed to match \'{0}\' when parsing \'{1}\''.format(final_fmt_pattern, string))
    parts = {}
    for token in tokens:
        if token == 'Do':
            value = match.group('value')
        else:
            value = match.group(token)
        parse_token(token, value, parts, locale)
    return build_datetime(parts)


def parse_token(token, value, parts, locale):
    if token == 'YYYY':
        parts['year'] = int(value)
    elif token == 'YY':
        value = int(value)
        parts['year'] = 1900 + value if value > 68 else 2000 + value

    elif token in ['MMMM', 'MMM']:
        parts['month'] = locale.month_number(value.lower())

    elif token in ['MM', 'M']:
        parts['month'] = int(value)

    elif token in ['DD', 'D']:
        parts['day'] = int(value)

    elif token in ['Do']:
        parts['day'] = int(value)

    elif token.upper() in ['HH', 'H']:
        parts['hour'] = int(value)

    elif token in ['mm', 'm']:
        parts['minute'] = int(value)

    elif token in ['ss', 's']:
        parts['second'] = int(value)

    elif token == 'SSSSSS':
        parts['microsecond'] = int(value)
    elif token == 'SSSSS':
        parts['microsecond'] = int(value) * 10
    elif token == 'SSSS':
        parts['microsecond'] = int(value) * 100
    elif token == 'SSS':
        parts['microsecond'] = int(value) * 1000
    elif token == 'SS':
        parts['microsecond'] = int(value) * 10000
    elif token == 'S':
        parts['microsecond'] = int(value) * 100000

    elif token == 'X':
        parts['timestamp'] = int(value)

    elif token in ['ZZZ', 'ZZ', 'Z']:
        parts['tzinfo'] = parse_tzinfo(value)

    elif token in ['a', 'A']:
        if value in (
                locale.meridians['am'],
                locale.meridians['AM']
        ):
            parts['am_pm'] = 'am'
        elif value in (
                locale.meridians['pm'],
                locale.meridians['PM']
        ):
            parts['am_pm'] = 'pm'


def build_datetime(parts):
    timestamp = parts.get('timestamp')

    if timestamp:
        return datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)

    am_pm = parts.get('am_pm')
    hour = parts.get('hour', 0)

    if am_pm == 'pm' and hour < 12:
        hour += 12
    elif am_pm == 'am' and hour == 12:
        hour = 0

    return datetime.datetime(year=parts.get('year', 1), month=parts.get('month', 1),
                             day=parts.get('day', 1), hour=hour, minute=parts.get('minute', 0),
                             second=parts.get('second', 0), microsecond=parts.get('microsecond', 0),
                             tzinfo=parts.get('tzinfo'))


def parse_multiformat(string, formats):
    _datetime = None

    for fmt in formats:
        try:
            _datetime = parse(string, fmt)
            break
        except:
            pass

    if _datetime is None:
        raise ParserError('Could not match input to any of {0} on \'{1}\''.format(formats, string))

    return _datetime


def parse_tzinfo(string):
    """Find the tzinfo object associated with a string."""
    if string.upper() == 'UTC':
        return pytz.utc

    # ISO match searches for a string in format '+04:00'
    iso_match = RES['tzinfo'].match(string)
    if iso_match:
        sign, hours, minutes = iso_match.groups()
        if minutes is None:
            minutes = 0

        sign = -1 if sign == '-' else 1
        hours, minutes = int(hours), int(minutes)

        tzinfo = datetime.timezone(sign * datetime.timedelta(hours=hours,
                                                             minutes=minutes))

    # If not, it might be something like 'US/Eastern' that tzinfo can parse..
    else:
        tzinfo = pytz.timezone(string)

    if tzinfo is None:
        raise ParserError('Could not parse timezone expression "{0}"', string)

    return tzinfo
