Saturn: Simple functions for tz-aware datetimes
===============================================

Performs common operations on datetimes with clean syntax, acting as a thin wrapper
for datetime and pytz. Force timezone-aware
datetimes. All operations are top-level functions: No dealing with
methods from multiple modules and objects.

There are several existing modules designed to improve Python's datetime functionality.
Here's why Saturn is different:

 - Uses native datetime.datetime and datetime.timedelta types for compatibility and speed
 - Only one import required
 - Clean, intuitive syntax and function names.  No boilerplate.
 - Operates exclusively with top-level functions; no sorting through methods
   from multiple objects and modules
 - Raises an exception if a func is given a tz-naive datetime as input. All datetime
   outputs are timezone-aware, with an easily-set TZ, defaulting to UTC.

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
 - time: Same concept as datimetime; easily create a tz-aware time.
 - now: Find current utc time; timezone-aware.
 - range_dt: Iterate over datetimes, with a customizable interval. Similar to builtin range. Lazy.
 - fix_naive: Convert a timezone-naive datetime to an aware one.
 - move_tz: Change a datetime from one timezone to another.
 - combine: Similar to datetime.datetime.combine, but always tz-aware.
 - to_str: Similar to datetime.datetime.strftime, but with a cleaner format string, from Arrow.
 - from_str: Similar to datetime.datetime.strptime, but with a cleaner format string, from Arrow.
 - to_iso: Wrapper for datetime.datetime's isoformat() method, as a function.
 - from_iso: Create a datetime from an isoformat string.
 - to_epoch: Wrapper for datetime.datetime's timestamp method, as a function.
 - from_epoch: Wrapper for datetime.datetime's from_timestamp method, as a function.
 - timedelta, date, and today are included as wrappers for their respective datetime/date classes, so you don't need to import datetime.


Installation
------------

.. code-block:: python

    pip install saturn


Basic documentation
-------------------

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


Function input and output:
--------------------------

.. code-block:: python

    datetime(year: int, month: int, day: int, hour: int=0, minute: int=0,
             second: int=0, microsecond: int=0, tzinfo=None, tz=None) -> datetime.datetime

    time(hour: int, minute: int=0, second: int=0,
         microsecond: int=0, tzinfo=None, tz=None) -> datetime.time

    now() -> datetime.datetime

    combine(_date: _datetime.date, _time: _datetime.time, tz: str='UTC') -> datetime.datetime

    fix_naive(dt: TimeOrDatetime, tz: str='UTC') -> datetime.datetime

    to_str(dt: DateOrDatetime, str_format: str) -> str

    from_str(dt_str: str, str_format: str, tz: str='UTC') -> datetime.datetime

    to_iso(dt: DateOrDatetime) -> str

    from_iso(iso_str: str, tz: str='UTC') -> datetime.datetime

    to_epoch(dt: DateOrDatetime) -> float:

    from_epoch(epoch: float, tz: str='UTC') -> _datetime.datetime:

    move_tz(dt: datetime.datetime, tz: str) -> datetime.datetime

    range_dt(start: DateOrDatetime, end: DateOrDatetime, step: int=1,
             interval: str='day') -> Iterator[datetime.datetime]



Some syntax we're dodging:
--------------------------


.. code-block:: python

        pytz.timezone('Europe/Berlin').localize(datetime.datetime(1985, 2, 1, 13, 21))

        arrow.Arrow(1999, 9, 9, 9, 30, tzinfo=dateutil.tz.gettz('US/Eastern'))

        pytz.timezone('US/Mountain').localize(datetime.datetime.combine(date, time))

        aware_dt.astimezone(pytz.timezone('US/Pacific'))


Replaced by:
------------


.. code-block:: python

        saturn.datetime(1985, 2, 1, 13, 21, tz='Europe/Berlin')

        saturn.datetime(1999, 9, 9, 9, 30, tz='US/Eastern')

        saturn.combine(date, time, 'US/Mountain')

        saturn.move_tz(aware_dt, 'US/Pacific')


