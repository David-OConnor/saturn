Saturn: Functions for better datetimes
======================================


Perform common operations on datetimes with clean syntax, acting as a thin wrapper
for datetime and pytz. Force timezone-aware
datetimes. All operations are top-level functions: No dealing with
a methods from multiple modules and objects.

There are several existing modules designed to improve Python's datetime functionality.
Here are some reasons why Saturn is different:

 - Uses native datetime.datetime and datetime.timedelta types for compatibility and speed
 - Only one import required
 - Clean, intuitive syntax and function names
 - Operates exclusively with top-level functions; no sorting through methods
   from multiple objects and modules

Saturn uses Pytz for timezones:
`Pytz website <https://pypi.python.org/pypi/pytz/>`_
Pytz is licensed under the MIT license.

... and Arrow for string formatting:
`Arrow website: <http://arrow.readthedocs.io/en/latest/>`_
Arrow is licensed under Apache 2.

Python 2 is currently unsupported.

Included functions
------------------

 - datetime: Return a timezone-aware datetime.datetime object.  Created the same way as datetime.datetime,
   with an optional 'tz' argument for a timezone string.
 - to_str: Similar to datetime.datetime.strftime, but with a cleaner format string, and as a function.
 - from_str: Similar to datetime.datetime.strptime, but with a cleaner format string, and as a function.
 - now: Find current utc time; timezone-aware
 - range_dt: Iterate over datetimes, with a customizable interval. Similar to builtin range. Lazy.
 - fix_naive: Convert a timezone-naive datetime to an aware one.
 - move_tz: Change a datetime from one timezone to another.
 - timedelta: Same as datetime.timedelta; you don't have to import datetime.


Installation
------------

.. code-block:: python

    pip install saturn


Basic documentation
-------------------

Create a timezone-aware datetime. If you don't specify a 'tz' argument, it defaults
to UTC.:

.. code-block:: python

    saturn.datetime(2016, 1, 1, 16, tz='US/Eastern')
    # datetime.datetime(2016, 1, 1, 16, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)

    saturn.datetime(2016, 1, 1, 16)
    # datetime.datetime(2016, 1, 1, 16, 0, tzinfo=<UTC>)


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


Convert a datetime a string. Uses format from moment.js:

.. code-block:: python

    saturn.to_str(saturn.now(), 'YYYY-MM-DD hh:mm')
    # '2016-04-29 03:30'


Convert a string to a datetime. Uses format from moment.js:

.. code-block:: python

    saturn.from_str('2016-04-29 03:30', 'YYYY-MM-DD hh:mm')
    # datetime.datetime(2016, 4, 29, 3, 30, tzinfo=<UTC>)


Convert a datetime a an ISO-8601-format string:

.. code-block:: python

        saturn.to_iso(saturn.now())
        # '2016-04-29T20:12:05.807558+00:00'


Some syntax we're dodging:
--------------------------


.. code-block:: python

        pytz.timezone('US/Eastern').localize(datetime.datetime.utcnow())
        arrow.Arrow(1999, 9, 9, 9, 30, tzinfo=dateutil.tz.gettz('US/Eastern'))
