import pytest
from date import Date, TimeDelta


@pytest.mark.parametrize("day, month, year", [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1)
])
def test_init_date_incorrect(day, month, year):
    with pytest.raises(ValueError):
        Date(day, month, year)
    with pytest.raises(ValueError):
        Date("30.02.1")


@pytest.mark.parametrize("day, month, year", [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (None, None, None)
])
def test_init_timedelta(day, month, year):
    test_timedelta = TimeDelta(day, month, year)
    assert test_timedelta.days == day
    assert test_timedelta.months == month
    assert test_timedelta.years == year


def test_repr_str_timedelta():
    test_timedelta = TimeDelta(1, 1, 1)
    assert repr(test_timedelta) == "TimeDelta(1, 1, 1)"
    assert str(test_timedelta) == "1 day(s), 1 month(s), 1 year(s)"


def test_correct_str_date():
    test_date = Date("3.3.3")


def test_incorrect_date():
    with pytest.raises(ValueError):
        Date("3.3")
    with pytest.raises(ValueError):
        Date(3, 3)


def test_str_repr_date():
    test_date = Date(1, 1, 1)
    assert repr(test_date) == "Date(1, 1, 1)"
    assert str(test_date) == "01.01.0001"


def test_leap():
    answers = []
    for year in (1, 100, 400, 1000, 2001):
        test_date = Date(11, 2, year)
        answers.append(test_date.is_leap_year(year))
    assert answers == [False, False, True, False, False]
    with pytest.raises(ValueError):
        test_date.is_leap_year("f")


@pytest.mark.parametrize("day", [0, 32])
def test_is_valid(day):
    test_date = Date(1, 1, 1)
    with pytest.raises(ValueError):
        test_date.is_valid_date(day, 1, 1)


def test_day_setter():
    test_date = Date(1, 1, 1)
    test_date.day = 4
    with pytest.raises(ValueError):
        test_date.day = 33


def test_month_setter():
    test_date = Date(1, 1, 1)
    test_date.month = 4
    with pytest.raises(ValueError):
        test_date.month = 33


def test_year_setter():
    test_date = Date(1, 1, 1)
    test_date.year = 4
    with pytest.raises(ValueError):
        test_date.year = 0


def test_sub():
    test_date1 = Date(11, 11, 1111)
    test_date2 = Date(12, 12, 1112)
    assert test_date1 - test_date2 == -398
    test_date2 = Date(12, 12, 400)
    assert test_date1 - test_date2 == 259654


def test_some_test():
    test_date1 = Date(11, 11, 1111)
    test_date2 = "OLOLO"
    res = test_date1.__sub__(test_date2)
    assert res == NotImplemented


def test_add():
    test_date = Date(11, 11, 1111)
    timedelta = TimeDelta(2000, 1, 1)
    summ = test_date + timedelta
    assert str(summ) == "03.06.1118"
    test_date = Date(28, 2, 400)
    timedelta = TimeDelta(2, 11, 400)
    summ = test_date + timedelta
    assert str(summ) == "01.02.0801"
    test_date = Date(1, 10, 1)
    timedelta = TimeDelta(30, 1, 0)
    summ = test_date + timedelta
    assert str(summ) == "01.12.0001"


def test_iadd():
    test_date = Date(11, 11, 1111)
    timedelta = TimeDelta(1, 1, 1)
    test_date += timedelta
    assert str(test_date) == "12.12.1112"
    test_date = Date(28, 2, 400)
    timedelta = TimeDelta(2, 9, 400)
    test_date += timedelta
    assert str(test_date) == "01.12.0800"
    test_date = Date(31, 12, 400)
    timedelta = TimeDelta(1, 0, 0)
    test_date += timedelta
    assert str(test_date) == "01.01.0401"
