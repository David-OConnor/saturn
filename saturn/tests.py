import datetime

import pytz

import saturn

# todo run checks by setting tzinfo and dates/times
# todo directly instead of localize/astiemzone when possible.


def test_dt_creation():
    dt = saturn.datetime(2016, 1, 1, 16, 9, 30, 10, tz='US/Eastern')
    assert dt == pytz.timezone('US/Eastern').localize(
        datetime.datetime(2016, 1, 1, 16, 9, 30, 10))

    dt = saturn.datetime(2016, 1, 1, 16, 9, 30, 10)
    assert dt == datetime.datetime(2016, 1, 1, 16, 9, 30, 10,
                                   tzinfo=pytz.utc)


def test_saturn_creation_with_tzinfo():
    dt = saturn.datetime(1823, 3, 2, 12, 0, tzinfo=pytz.utc, tz='US/Eastern')
    baseline = datetime.datetime(1823, 3, 2, 12, 0, tzinfo=pytz.utc)
    assert dt == baseline


def test_time_creation():
    time = saturn.time(12, 30, 30, 201)
    assert time == datetime.time(12, 30, 30, microsecond=201,
                                 tzinfo=pytz.utc)


def test_fix_naive():
    naive = datetime.datetime(year=2016, month=12, day=9, second=2)
    fixed = saturn.fix_naive(naive)
    assert fixed == datetime.datetime(2016, 12, 9, 0, 0, 2, tzinfo=pytz.utc)


def test_move():
    dt = saturn.datetime(1293, 1, 1, tz='Asia/Gaza')
    moved = saturn.move_tz(dt, 'Europe/Vatican')

    baseline_dt = pytz.timezone('Asia/Gaza').localize(
        datetime.datetime(1293, 1, day=1))
    baseline_moved = baseline_dt.astimezone(pytz.timezone('Europe/Vatican'))
    assert moved == baseline_moved


def test_to_str():
    format_str = 'dddd MMMM d, YYYY. hh:mm::ss. ZZ'
    formatted = saturn.to_str(saturn.datetime(2009, 2, 3, hour=20, minute=31, second=2),
                              format_str)
    assert formatted == 'Tuesday February 2, 2009. 08:31::02. -00:00'


def from_str():
    format_str = 'dddd MMMM d, YYYY. hh:mm::ss. ZZ'
    dt = saturn.from_str('Tuesday February 2, 2009. 08:31::02. -00:00', format_str)
    baseline = datetime.datetime(2009, 2, 1, 8, 31, 2, tzinfo=pytz.utc)
    assert dt == baseline


def test_combine():
    date, time = datetime.date(2016, 3, 2), datetime.time(16, 30)
    baseline = datetime.datetime(2016, 3, 2, 16, 30, tzinfo=pytz.utc)
    assert saturn.combine(date, time) == baseline


def test_split():
    dt = saturn.datetime(2016, 3, 2, 16, 30, 1, 500, tz='US/Mountain')
    date, time = saturn.split(dt)

    baseline_date = datetime.date(2016, 3, 2)
    baseline_time = datetime.time(16, 30, 1, 500, pytz.timezone('US/Mountain'))

    assert date == baseline_date
    assert time == baseline_time

    # todo test iterate
