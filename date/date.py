from typing import Optional, overload


class TimeDelta:
    def __init__(self, days: Optional[int] = None, months: Optional[int] = None, years: Optional[int] = None):
        self.days = days
        self.months = months
        self.years = years

    def __repr__(self) -> str:
        """Возвращает timedelta в формате TimeDelta(day, month, year)"""
        return f"TimeDelta({self.days}, {self.months}, {self.years})"

    def __str__(self) -> str:
        """Возвращает timedelta в формате dd, mm, yyyy"""
        return str(f'{self.days} day(s), {self.months} month(s), {self.years} year(s)')


class Date:
    """Класс для работы с датами"""
    days_in_month = (31, (28, 29), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @overload
    def __init__(self, day: int, month: int, year: int):
        """Создание даты из трех чисел"""

    @overload
    def __init__(self, date: str):
        """Создание даты из строки формата dd.mm.yyyy"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            values = args[0].split(".")
            if len(values) != 3:
                raise ValueError("Incorrect input date format")
            else:
                self.is_valid_date(int(values[0]), int(values[1]), int(values[2]))
                self._day = int(values[0])
                self._month = int(values[1])
                self._year = int(values[2])

        elif len(args) == 3:
            self.is_valid_date(args[0], args[1], args[2])
            self._day = args[0]
            self._month = args[1]
            self._year = args[2]
        else:
            raise ValueError("Incorrect date format")

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        return str(f'{self._day:02d}.{self._month:02d}.{self._year:04d}')

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""
        return f"Date({self._day}, {self._month}, {self._year})"

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Проверяет, является ли год високосным"""
        if not isinstance(year, int):
            raise ValueError("Year must be integer type")
        else:
            if year % 100 == 0 and year % 400 != 0:
                return False
            elif year % 4 == 0:
                return True
            else:
                return False

    def get_max_day(self, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""
        if month == 2:
            return self.days_in_month[month - 1][self.is_leap_year(year)]
        else:
            return self.days_in_month[month-1]


    def is_valid_date(self, day: int, month: int, year: int):
        """Проверяет, является ли дата корректной"""
        if month > 12 or month < 1:
            raise ValueError("Incorrect month")
        if year < 1:
            raise ValueError("Incorrect year")
        if day > self.get_max_day(month, year) or day < 1:
            raise ValueError(f"Invalid day {day} of month {month} for year {year}")
        return True

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """value от 1 до 31. Проверять значение и корректность даты"""
        if 1 <= value <= 31:
            self.is_valid_date(value, self._month, self._year)
            self._day = value
        else:
            raise ValueError("Incorrect day")

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """value от 1 до 12. Проверять значение и корректность даты"""
        if 1 <= value <= 12:
            self.is_valid_date(self._day, value, self._year)
            self._month = value
        else:
            raise ValueError("Incorrect month")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """value от 1 до ... . Проверять значение и корректность даты"""
        if 1 <= value:
            self.is_valid_date(self._day, self._month, value)
            self._year = value
        else:
            raise ValueError("Incorrect year")

    def convert_to_days(self, day: int, month: int, year: int) -> int:
        """Возвращает количество дней в дате"""
        days_from_days = day
        days_from_month = 0
        for mon in range(month):
            if mon == 1:
                day_num = self.days_in_month[1][self.is_leap_year(year)]
            else:
                day_num = self.days_in_month[mon]
            days_from_month += day_num

        days_from_years, day_num = 0, 0
        for y in range(year):
            if self.is_leap_year(y):
                days_from_years += 366
            else:
                days_from_years += 365
        return days_from_days+days_from_month+days_from_years

    def __sub__(self, other: "Date") -> int:
        """Разница между датой self и other (-)"""
        if not isinstance(other, Date):
            return NotImplemented
        day_num1 = self.convert_to_days(self._day, self._month, self._year)
        day_num2 = self.convert_to_days(other._day, other._month, other._year)
        return day_num1 - day_num2

    def __add__(self, other: TimeDelta) -> "Date":
        """Складывает self и некий timedeltа. Возвращает НОВЫЙ инстанс Date, self не меняет (+)"""
        added_days = other.days
        added_months = other.months
        added_years = other.years
        month_count = self._month
        days_count = self._day
        year_count = 0
        while added_days + days_count > self.get_max_day(month_count, self._year + year_count):
            added_days = added_days + days_count - self.get_max_day(month_count, self._year + year_count)
            added_months += 1
            month_count += 1
            if month_count == 13:
                month_count = 1
                year_count += 1
            days_count = 0
        result_days = added_days + days_count
        while self._month + added_months > 12:
            added_years += 1
            added_months -= 12
        result_month = self._month + added_months
        result_year = self._year + added_years

        if result_days > self.get_max_day(result_month, result_year):
            result_days -= self.get_max_day(result_month, result_year)
            result_month += 1
        return Date(result_days, result_month, result_year)

    def __iadd__(self, other: TimeDelta):
        """Добавляет к self некий timedelta меняя сам self (+=)"""
        result_date = self + other
        self._day = result_date.day
        self._month = result_date.month
        self._year = result_date.year
        return self


def _main():
    print("Hello =)")
    date1 = Date(28,2,4)
    date1.day = 2
    date1 += TimeDelta(366, 36, 0)
    print(date1)


if __name__ == '__main__':
    _main()