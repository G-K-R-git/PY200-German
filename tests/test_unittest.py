from date import Date, TimeDelta
import unittest


class MyTestCase(unittest.TestCase):

    def test_init(self):
        for i in (-1, 1, 32):
            date = i
            for j in (-1, 1, 13):
                month = j
                for k in (0, 1):
                    if i == 1 and j == 1 and k == 1:
                        pass
                    else:
                        year = k
                        with self.assertRaises(ValueError):
                            some_date = Date(date, month, year)
        date1, month1, year1 = 1, 1, 1
        with self.assertRaises(ValueError):
            Date(date1, month1)
        with self.assertRaises(ValueError):
            Date("2.2")
        self.assertEqual(str(Date("2.2.2")), "02.02.0002")

    def test_repr(self):
        date = 1
        month = 1
        year = 1
        test_date = Date(date, month, year)
        test_timedelta = TimeDelta(date, month, year)
        self.assertEqual(test_date.__repr__(), f"Date({date}, {month}, {year})", "Should be 'Date(1, 1, 1)'")
        self.assertEqual(test_timedelta.__repr__(), f"TimeDelta({date},"
                                                    f" {month}, {year})", "Should be 'TimeDelta(1, 1, 1)'")

    def test_str(self):
        day, month, year = 1, 1, 1
        test_date = Date(day, month, year)
        test_timedelta = TimeDelta(day, month, year)
        self.assertEqual(str(test_date), "01.01.0001")
        self.assertEqual(str(test_timedelta), f'{day} day(s), {month} month(s), {year} year(s)')
        day, month, year = 11, 1, 1
        test_date = Date(day, month, year)
        test_timedelta = TimeDelta(day, month, year)
        self.assertEqual(str(test_date), "11.01.0001")
        self.assertEqual(str(test_timedelta), f'{day} day(s), {month} month(s), {year} year(s)')
        day, month, year = 11, 11, 1
        test_date = Date(day, month, year)
        test_timedelta = TimeDelta(day, month, year)
        self.assertEqual(str(test_date), "11.11.0001")
        self.assertEqual(str(test_timedelta), f'{day} day(s), {month} month(s), {year} year(s)')
        day, month, year = 11, 11, 11
        test_date = Date(day, month, year)
        test_timedelta = TimeDelta(day, month, year)
        self.assertEqual(str(test_date), "11.11.0011")
        self.assertEqual(str(test_timedelta), f'{day} day(s), {month} month(s), {year} year(s)')
        year = 111
        test_date = Date(day, month, year)
        test_timedelta = TimeDelta(day, month, year)
        self.assertEqual(str(test_date), "11.11.0111")
        self.assertEqual(str(test_timedelta), f'{day} day(s), {month} month(s), {year} year(s)')
        year = 1111
        test_date = Date(day, month, year)
        test_timedelta = TimeDelta(day, month, year)
        self.assertEqual(str(test_date), "11.11.1111")
        self.assertEqual(str(test_timedelta), f'{day} day(s), {month} month(s), {year} year(s)')

    def test_is_leap_year(self):
        answers = []
        for year in (1, 100, 400, 1000, 2001):
            test_date = Date(11, 11, year)
            answers.append(test_date.is_leap_year(year))
        self.assertEqual(answers, [False, False, True, False, False])
        with self.assertRaises(ValueError):
            test_date.is_leap_year("f")

    def test_get_max_days(self):
        j = 1
        for i in (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31):
            test_date = Date(11, j, 400)
            self.assertEqual(test_date.get_max_day(test_date.month, test_date.year), i)
            j += 1
        j = 1
        for i in (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31):
            test_date = Date(11, j, 401)
            self.assertEqual(test_date.get_max_day(test_date.month, test_date.year), i)
            j += 1

    def test_is_valid_date(self):
        with self.assertRaises(ValueError):
            Date(29, 2, 401)

    def test_setters(self):
        test_date = Date(11, 11, 1111)
        test_date.day = 12
        test_date.month = 12
        test_date.year = 1112
        test_date = Date(1, 1, 1)

    def test_setters_incorrect(self):
        test_date = Date(1, 1, 1)
        with self.assertRaises(ValueError):
            test_date.day = 32
        with self.assertRaises(ValueError):
            test_date.month = 13
        with self.assertRaises(ValueError):
            test_date.year = 0

    def test_sub(self):
        test_date1 = Date(11, 11, 1111)
        test_date2 = Date(12, 12, 1112)
        self.assertEqual(test_date1 - test_date2, -398)
        test_date2 = Date(12, 12, 400)
        self.assertEqual(test_date1 - test_date2, 259654)

    def test_sub_incorrect(self):
        test_date1 = Date(11, 11, 1111)
        test_date2 = "OLOLO"
        res = test_date1.__sub__(test_date2)
        self.assertEqual(res, NotImplemented)

    def test_add(self):
        test_date = Date(11, 11, 1111)
        timedelta = TimeDelta(1, 1, 1)
        summ = test_date + timedelta
        self.assertEqual(str(summ), "12.12.1112")
        test_date = Date(28, 2, 400)
        timedelta = TimeDelta(2, 11, 400)
        summ = test_date + timedelta
        self.assertEqual(str(summ), "01.02.0801")
        test_date = Date(1, 10, 1)
        timedelta = TimeDelta(30, 1, 0)
        summ = test_date + timedelta
        self.assertEqual(str(summ), "01.12.0001")

    def test_iadd(self):
        test_date = Date(11, 11, 1111)
        timedelta = TimeDelta(1, 1, 1)
        test_date += timedelta
        self.assertEqual(str(test_date), "12.12.1112")
        test_date = Date(28, 2, 400)
        timedelta = TimeDelta(2, 9, 400)
        test_date += timedelta
        self.assertEqual(str(test_date), "01.12.0800")
        test_date = Date(31, 12, 400)
        timedelta = TimeDelta(1, 0, 0)
        test_date += timedelta
        self.assertEqual(str(test_date), "01.01.0401")


if __name__ == '__main__':
    unittest.main(verbosity=2)
