Instant: Functions for better datetimes
=======================================


Perform common operations on datetimes with clean syntax. Force timezone-aware
datetimes. All operations are top-level functions: No dealing with
a methods from multiple modules and objects. Only one import required.

There are several existing modules designed to improve Python's datetime functionality.
Here are some reasons why Instant is different:

 - Uses native datetime.datetime objects for compatibility and speed
 - Only one import required
 - Clean, intuitive syntax and function names
 - Operates exclusively with top-level functions; no sorting through methods
   from multiple objects and modules

`Pytz website <https://pypi.python.org/pypi/pytz/>`_

Python 2 is currently unsupported.

Included functions
------------------

 - datetime: Return a timezone-aware datetime.datetime object.  Created the same way as datetime.datetime,
   with an optional 'tz' argument for a timezone string.
 - to_str: Similar to datetime.datetime.strftime, but with a cleaner format string, and as a function.
 - from_str: Similar to datetime.datetime.strptime, but with a cleaner format string, and as a function.
 - now: Find current utc time; timezone-aware
 - range_dt: Iterate over datetimes, with a customizable interval. Similar to builtin range.
 - fix_naive: Convert a timezone-naive datetime to an aware one.
 - move_tz: Change a time from one timezone to another.


Basic documentation
-------------------

Create a timezone-aware datetime. If you don't specify a 'tz' argument, it defaults
to UTC.:

.. code-block:: python

    instant.datetime(2016, 1, 1, 16, tz='US/Eastern')
    # datetime.datetime(2016, 1, 1, 16, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)

    instant.datetime(2016, 1, 1, 16)
    # datetime.datetime(2016, 1, 1, 16, 0, tzinfo=<UTC>)


Make a tz-naive datetime aware:

.. code-block:: python

    naive = datetime.datetime(2016, 1, 1)
    instant.fix_naive(naive, "Pacific/Midway")
    # datetime.datetime(2016, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Pacific/Midway' SST-1 day, 13:00:00 STD>)


Find the current datetime, in UTC:

.. code-block:: python

    instant.now()
    # datetime.datetime(2016, 4, 29, 20, 36, 53, 257753, tzinfo=<UTC>)


Iterate through a range of datetimes. Valid intervals are 'week', 'month', 'day'
'hour', 'minute', 'second', 'millisecond', and 'microsecond':

.. code-block:: python

    start, end = instant.datetime(2016, 1, 2, 12, 30), instant.datetime(2016, 1, 5, 12, 30)
    for dt in instant.range_dt(start, end, interval='day'):
        print(dt)

    # 2016-01-02 12:30:00+00:00
    # 2016-01-03 12:30:00+00:00
    # 2016-01-04 12:30:00+00:00

    for dt in instant.range_dt(start, end, 4, interval='hour'):
        print(dt)

    # 2016-01-02 12:30:00+00:00
    # 2016-01-02 16:30:00+00:00
    # 2016-01-02 20:30:00+00:00
    ...
    # 2016-01-05 00:30:00+00:00
    # 2016-01-05 04:30:00+00:00
    # 2016-01-05 08:30:00+00:00


Convert a datetime a string. Uses format from Arrow:

.. code-block:: python

    instant.to_str(instant.now(), 'YYYY-MM-DD hh:mm')
    # '2016-04-29 03:30'


Convert a string to a datetime. Uses format from Arrow:

.. code-block:: python

    instant.to_str('2016-04-29 03:30', 'YYYY-MM-DD hh:mm')
    # datetime.datetime(2016, 4, 29, 3, 30, tzinfo=<UTC>)


Convert a datetime a an ISO-8601-format string:

.. code-block:: python

        instant.to_iso(instant.now())
        # '2016-04-29T20:12:05.807558+00:00'
