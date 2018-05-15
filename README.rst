Saturn: Simple functions for tz-aware datetimes
===============================================

Performs common operations on datetimes with clean syntax, acting as a thin wrapper
for datetime and pytz. Force timezone-aware
datetimes. All operations are top-level functions: No dealing with
methods from multiple modules and objects.

There are several existing modules designed to improve Python's datetimes.
Here's why Saturn is different:

 - Uses native datetime types for compatibility and speed
 - Only one import required
 - Clean, intuitive syntax and function names.  No boilerplate.
 - Operates exclusively with top-level functions; no sorting through methods
   from multiple objects and modules
 - Raises an exception if a func is given a tz-naive datetime as input. All datetime
   outputs are timezone-aware, with an easily-set TZ, defaulting to UTC.

This project doesn't tackle the deeper problems with Python's datetimes that can arise
from timezone and localization conflicts. It aims to make working with dateimtes easier by providing a
concise, consistent, and expressive API; and preventing naive datetimes from entering your code.

Saturn uses Pytz for timezones. Used as a dependency.:
`Pytz website <https://pypi.python.org/pypi/pytz/>`_
Pytz is licensed under the MIT license.

... and uses code from Arrow for string formatting and parsing. Not a dependency.:
`Arrow website: <http://arrow.readthedocs.io/en/latest/>`_
Arrow is licensed under Apache 2.

Python 2 is unsupported.

Included functions
------------------

 - datetime: Return a timezone-aware datetime.datetime object.  Created the same way as datetime.datetime,
   with an optional 'tz' argument for a timezone string. Defaults to UTC.
 - time: Same concept as datetime.time; easily create a tz-aware time.
 - now: Find current utc time; timezone-aware.
 - range_dt: Iterate over datetimes, with a customizable interval. Similar to builtin range. Lazy.
 - fix_naive: Convert a timezone-naive datetime to an aware one.
 - move_tz: Change a datetime from one timezone to another.
 - combine: Similar to datetime.datetime.combine, but always tz-aware.
 - to_str: Similar to datetime.datetime.strftime, but with a cleaner format string, from Arrow.
 - from_str: Similar to datetime.datetime.strptime, but with a cleaner format string, from Arrow.
   Returns date, datetime, or time objects as needed.
 - to_iso: Wrapper for datetime.datetime's isoformat() method, as a function.
 - from_iso: Create a datetime from an isoformat string.
 - to_epoch: Wrapper for datetime.datetime's timestamp method, as a function.
 - from_epoch: Wrapper for datetime.datetime's from_timestamp method, as a function.
 - split: Split a datetime into date and time components.  Useful because datetime's .time() method strips timezone info.
 - add, subtract: Add or subtract to/from a datetime.
 - overlaps: Deterine if two date/time/datetime ranges overlap.
 - timedelta, date, and today are included as wrappers for their respective datetime/date classes, so you don't need to import datetime.


Installation
------------

.. code-block:: bash

    pip install saturn


Documentation
-------------

Create a timezone-aware datetime. If you don't specify a 'tz' argument, it defaults
to UTC. Works for times too:

.. code-block:: python

    saturn.datetime(2016, 1, 1, 16, tz='US/Eastern')
    # datetime.datetime(2016, 1, 1, 16, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)

    saturn.datetime(2016, 1, 1, 16)
    # datetime.datetime(2016, 1, 1, 16, 0, tzinfo=<UTC>)

    saturn.time(11, 29, 30)
    # datetime.time(11, 29, 30, tzinfo=<UTC>)


Make a tz-naive datetime aware:

.. code-block:: python

    naive = datetime.datetime(2016, 1, 1)
    saturn.fix_naive(naive, "Pacific/Midway")
    # datetime.datetime(2016, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Pacific/Midway' SST-1 day, 13:00:00 STD>)


Find the current datetime, in UTC:

.. code-block:: python

    saturn.now()
    # datetime.datetime(2016, 4, 29, 20, 36, 53, 257753, tzinfo=<UTC>)


Move from one timezone to another:

.. code-block:: python

    dt = saturn.datetime(2016,1,1, tz='Asia/Gaza')
    # datetime.datetime(2016, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Asia/Gaza' EET+2:00:00 STD>)

    saturn.move_tz(dt, 'Europe/Vatican')
    # datetime.datetime(2015, 12, 31, 23, 0, tzinfo=<DstTzInfo 'Europe/Vatican' CET+1:00:00 STD>


Combine a date and time into a timezone-aware datetime. If the time is already aware, the 'tz' argument is ignored:

.. code-block:: python

    date, time = datetime.date(2016, 3, 2), datetime.time(16, 30)

    saturn.combine(date, time)
    # datetime.datetime(2016, 3, 2, 16, 30, tzinfo=<UTC>)

    saturn.combine(date, time, tz='Europe/London')
    # datetime.datetime(2016, 3, 2, 16, 30, tzinfo=<DstTzInfo 'Europe/London' GMT0:00:00 STD>)


Split a datetime into date and time components; keeps tzinfo, unlike datetime.time().

.. code-block:: python

    dt = saturn.datetime(2016, 3, 2, 16, 30, 1, 500, tz='US/Mountain')
    date, time = saturn.split(dt)
    # datetime.date(2016, 3, 2)
    # datetime.time(16, 30, 1, 500, tzinfo=<DstTzInfo 'US/Mountain' MST-1 day, 17:00:00 STD>)


Iterate through a range of datetimes. Valid intervals are 'week', 'month', 'day'
'hour', 'minute', 'second', 'millisecond', and 'microsecond':

.. code-block:: python

    start, end = saturn.datetime(2016, 1, 2, 12, 30), saturn.datetime(2016, 1, 5, 12, 30)
    for dt in saturn.range_dt(start, end, interval='day'):
        print(dt)

    # 2016-01-02 12:30:00+00:00
    # 2016-01-03 12:30:00+00:00
    # 2016-01-04 12:30:00+00:00

    for dt in saturn.range_dt(start, end, 4, interval='hour'):
        print(dt)

    # 2016-01-02 12:30:00+00:00
    # 2016-01-02 16:30:00+00:00
    # 2016-01-02 20:30:00+00:00
    ...
    # 2016-01-05 00:30:00+00:00
    # 2016-01-05 04:30:00+00:00
    # 2016-01-05 08:30:00+00:00


Convert a datetime to a string. Uses format from Arrow:

.. code-block:: python

    saturn.to_str(saturn.now(), 'YYYY-MM-DD hh:mm')
    # '2016-04-29 03:30'


Convert a string to a datetime. Uses format from Arrow. If the string includes a timezone, the optional tz argument is ignored:

.. code-block:: python

    saturn.from_str('2016-04-29 03:30', 'YYYY-MM-DD hh:mm')
    # datetime.datetime(2016, 4, 29, 3, 30, tzinfo=<UTC>)

    saturn.from_str('2016-04-29 03:30', 'YYYY-MM-DD hh:mm', tz='Africa/Cairo')
    # datetime.datetime(2016, 4, 29, 3, 30, tzinfo=<DstTzInfo 'Africa/Cairo' EET+2:00:00 STD>)

    saturn.from_str('1381685817', 'X')
    # datetime.datetime(2013, 10, 13, 17, 36, 57, tzinfo=<UTC>)


Convert a datetime to an ISO-8601 string or epoch:

.. code-block:: python

        saturn.to_iso(saturn.now())
        # '2016-04-29T20:12:05.807558+00:00'

        saturn.to_epoch(saturn.now())
        # 1461960725.807558


Convert an ISO-8601 string or epoch to a datetime:

.. code-block:: python

        saturn.from_iso('2016-04-29T20:12:05.000000+00:00')
        # datetime.datetime(2016, 4, 29, 20, 12, 05, tzinfo=<UTC>)

        saturn.from_epoch(1461960725)
        # datetime.datetime(2016, 4, 29, 21, 12, 5, tzinfo=<UTC>)


For details on to_str and from_str syntax, please reference `Arrow's formatting guide <http://arrow.readthedocs.io/en/latest/#tokens>`_.

Check if a range of times overlaps.

.. code-block:: python

        start1 = saturn.datetime(2018, 1, 1, 9)
        end1 = saturn.datetime(2018, 1, 1, 12)
        start2 = saturn.datetime(2018, 1, 1, 11)
        end2 = saturn.datetime(2018, 1, 1, 17)

        saturn.overlaps(start1, end1, start2, end2)
        # True
        saturn.overlaps(start1, end1, saturn.datetime(2018, 1, 1, 13), end2)
        # False


Function input and output:
--------------------------

.. code-block:: python

    datetime(year: float, month: float, day: float, hour: float=0, minute: float=0,
             second: float=0, microsecond: float=0, tzinfo=None, tz: str='UTC') -> datetime.datetime

    time(hour: float, minute: float=0, second: float=0,
         microsecond: float=0, tzinfo=None, tz: str='UTC') -> datetime.time

    now() -> datetime.datetime

    combine(_date: datetime.date, _time: _datetime.time, tz: str='UTC') -> datetime.datetime

    fix_naive(dt: TimeOrDatetime, tz: str='UTC') -> datetime.datetime

    to_str(dt: DateOrDatetime, str_format: str) -> str

    from_str(dt_str: str, str_format: str, tz: str='UTC') -> DateOrTimeOrDatetime

    to_iso(dt: DateOrDatetime) -> str

    from_iso(iso_str: str, tz: str='UTC') -> datetime.datetime

    to_epoch(dt: DateOrDatetime) -> float:

    from_epoch(epoch: float, tz: str='UTC') -> _datetime.datetime:

    move_tz(dt: datetime.datetime, tz: str) -> datetime.datetime

    add(dt: datetime.datetime, days: float=0, seconds: float=0, microseconds: float=0,
        milliseconds: float=0, minutes: float=0, hours: float=0, weeks: float=0) -> datetime.datetime

    subtract(dt: datetime.datetime, days: float=0, seconds: float=0, microseconds: float=0,
        milliseconds: float=0, minutes: float=0, hours: float=0, weeks: float=0) -> datetime.datetime

    range_dt(start: DateOrDatetime, end: DateOrDatetime, step: int=1,
             interval: str='day') -> Iterator[datetime.datetime]

    split(dt: datetime.datetime) -> Tuple[_datetime.date, _datetime.time]:

    overlaps(start1: DateOrTimeOrDatetime, start2: DateOrTimeOrDatetime,
             end1: DateOrTimeOrDatetime, end2: DateOrTimeOrDatetime) -> bool:



Some syntax we're dodging:
--------------------------


.. code-block:: python

        pytz.timezone('Europe/Berlin').localize(datetime.datetime(1985, 2, 1, 13, 21))

        arrow.Arrow(1999, 9, 9, 9, 30, tzinfo=dateutil.tz.gettz('US/Eastern'))

        pytz.timezone('US/Mountain').localize(datetime.datetime.combine(date, time))

        aware_dt.astimezone(pytz.timezone('US/Pacific'))

        aware_time = datetime.time(aware_dt.hour, aware_dt.minute, aware_dt.second,
            aware_dt.microsecond, aware_dt.tzinfo)


Replaced by:
------------


.. code-block:: python

        saturn.datetime(1985, 2, 1, 13, 21, tz='Europe/Berlin')

        saturn.datetime(1999, 9, 9, 9, 30, tz='US/Eastern')

        saturn.combine(date, time, 'US/Mountain')

        saturn.move_tz(aware_dt, 'US/Pacific')

        _, aware_time = saturn.split(aware_dt)


