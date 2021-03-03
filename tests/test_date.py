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
])
def test_init_timedelta(day, month, year):
    test_timedelta = TimeDelta(day, month, year)
    assert test_timedelta.days == day
    assert test_timedelta.months == month
    assert test_timedelta.years == year


def test_init_timedelta_incorrect():
    with pytest.raises(ValueError):
        test_timedelta = TimeDelta(None, None, None)


def test_repr_str_timedelta():
    test_timedelta = TimeDelta(1, 1, 1)
    assert repr(test_timedelta) == "TimeDelta(1, 1, 1)"
    assert str(test_timedelta) == "1 day(s), 1 month(s), 1 year(s)"


def test_correct_str_date():
    assert str(Date("3.3.3")) == "03.03.0003"


def test_incorrect_date():
    with pytest.raises(ValueError):
        Date("3.3")
    with pytest.raises(ValueError):
        Date(3, 3)


def test_str_repr_date():
    test_date = Date(1, 1, 1)
    assert repr(test_date) == "Date(1, 1, 1)"
    assert str(test_date) == "01.01.0001"


@pytest.mark.parametrize("year", [1, 100, 1000, 2001])
def test_is_not_leap(year):
    test_date = Date(11, 2, year)
    assert test_date.is_leap_year(test_date.year) == False


@pytest.mark.parametrize("year", [4, 400, 2000, 16])
def test_is_leap(year):
    test_date = Date(11, 2, year)
    assert test_date.is_leap_year(test_date.year) == True


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

@pytest.mark.parametrize("date1, date2, expected", [
    (Date(11, 11, 1111), Date(12, 11, 1111), -1),
    (Date(12, 11, 1111), Date(12, 11, 1111), 0),
    (Date(12, 12, 1111), Date(12, 11, 1111), 31),
    (Date(3, 1, 2222), Date(12, 11, 1111), 405473),
    (Date(1, 1, 1), Date(1, 1, 2), -365),
    (Date(1, 1, 4), Date(1, 1, 5), -366),
])
def test_sub(date1, date2, expected):
    assert date1 - date2 == expected


def test_some_test():
    test_date1 = Date(11, 11, 1111)
    test_date2 = "OLOLO"
    res = test_date1.__sub__(test_date2)
    assert res == NotImplemented


@pytest.mark.parametrize("date1, date2, expected", [
    (Date(11, 11, 1111), TimeDelta(2000, 1, 1), "03.06.1118"),
    (Date(28, 2, 400), TimeDelta(2, 11, 400), "01.02.0801"),
    (Date(1, 10, 1), TimeDelta(30, 1, 0), "01.12.0001"),
])
def test_add(date1, date2, expected):
    assert str(date1 + date2) == expected


@pytest.mark.parametrize("date1, date2, expected", [
    (Date(11, 11, 1111), TimeDelta(1, 1, 1), "12.12.1112"),
    (Date(28, 2, 400), TimeDelta(2, 9, 400), "01.12.0800"),
    (Date(31, 12, 400), TimeDelta(31, 12, 400), "31.01.0802"),
])
def test_iadd(date1, date2, expected):
    date1 += date2
    assert str(date1) == expected
