from typing import Optional, overload, Tuple, Any


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
        return str(f'{self.days} days, {self.months} months, {self.years} years')

class Date:
    """Класс для работы с датами"""
    days_in_month = (31, (28, 29), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @overload
    def __init__(self, day: int, month: int, year: int):
        """Создание даты из трех чисел"""

    @overload
    def __init__(self, date: str):
        """Создание даты из строки формата dd.mm.yyyy"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            values = args[0].split(".")
            if len(values) != 3:
                raise ValueError("Incorrect date format")
            else:
                self.month = int(values[1])
                self.year = int(values[2])
                self.day = int(values[0])
                self.is_valid_date(self._day, self._month, self._year)
        elif len(args) == 3:
            self.month = args[1]
            self.year = args[2]
            self.day = args[0]
            self.is_valid_date(self._day, self._month, self._year)
        else:
            raise ValueError("Incorrect date format")

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        if self._day < 10:
            day_str = f"0{self._day}"
        else:
            day_str = str(self._day)

        if self._month < 10:
            month_str = f"0{self._month}"
        else:
            month_str = str(self._month)

        if self._year < 10:
            year_str = f"000{self._year}"
        elif 10 <= self._year < 100:
            year_str = f"00{self._year}"
        elif 100 <= self._year < 1000:
            year_str = f"0{self._year}"
        else:
            year_str = str(self._year)

        return str(f'{day_str}.{month_str}.{year_str}')

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""
        return f"Date({self._day}, {self._month}, {self._year})"

    def is_leap_year(self, year: int) -> bool:
        """Проверяет, является ли год високосным"""
        if year % 100 == 0 and year % 400 != 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False

    def get_max_day(self, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""
        if month == 2 and not self.is_leap_year(year):
            return self.days_in_month[month-1][0]
        elif month == 2 and self.is_leap_year(year):
            return self.days_in_month[month-1][1]
        else:
            return self.days_in_month[month-1]

    def is_valid_date(self, day: int, month: int, year: int):
        """Проверяет, является ли дата корректной"""
        if day > self.get_max_day(month, year):
            raise ValueError(f"Invalid day {day} of month {month} for year {year}")

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """value от 1 до 31. Проверять значение и корректность даты"""
        if 1 <= value <= 31:
            self._day = value
            self.is_valid_date(self._day, self._month, self._year)
        else:
            raise ValueError("Incorrect day")

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """value от 1 до 12. Проверять значение и корректность даты"""
        if 1 <= value <= 12:
            self._month = value
        else:
            raise ValueError("Incorrect month")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """value от 1 до ... . Проверять значение и корректность даты"""
        if 0 <= value:
            self._year = value
        else:
            raise ValueError("Incorrect year")

    def convert_to_days(self, day: int, month: int, year: int) -> int:
        """Возвращает количество дней в дате"""
        days_from_days = day

        days_from_month = 0
        for mon in range(month):
            if mon == 1 and not self.is_leap_year(year):
                day_num = self.days_in_month[1][0]
            elif mon == 1 and self.is_leap_year(year):
                day_num = self.days_in_month[1][1]
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
        result_days = added_days
        while self._month + added_months > 12:
            added_years += 1
            added_months -= 12
        result_month = self._month + added_months
        result_year = self._year + added_years
        return Date(result_days, result_month, result_year)

    def __iadd__(self, other: TimeDelta) -> "Date":
        """Добавляет к self некий timedelta меняя сам self (+=)"""
        result_date = self.__add__(other)
        self._day = result_date.day
        self._month = result_date.month
        self._year = result_date.year


if __name__ == '__main__':
    # some_date1 = Date(30, 3, 3333)
    # print(some_date1.day, some_date1.month, some_date1.year, some_date1)
    # some_date2 = Date('12.12.1222')
    # print(some_date2.day, some_date2.month, some_date2.year)
    # some_date3 = Date('12.12')
    # print(some_date3.day, some_date3.month, some_date3.year)
    some_date4 = Date('2.2.4')
    print("One date is", some_date4)
    # print(some_date4.__str__())
    # print(some_date4.__repr__())
    some_date5 = Date(2, 2, 4)
    some_date5.day = 28
    print(some_date5, "Not a leap year" if not some_date5.is_leap_year(some_date5.year) else "Leap year")
    print("Number of days for year", some_date5.year, "in month", some_date5.month, ":", some_date5.get_max_day(some_date5.month, some_date5.year))
    print("Date is valid" if not some_date5.is_valid_date(some_date5.day, some_date5.month, some_date5.year) else "Date is invalid")

    print("days in some_date5:", some_date5.convert_to_days(some_date5.day, some_date5.month, some_date5.year))
    print("days in some_date4:", some_date4.convert_to_days(some_date4.day, some_date4.month, some_date4.year))
    print("difference is", some_date5.__sub__(some_date4), "days")

    timedelta1 = TimeDelta(33, 9, 1)
    print(some_date5.__repr__(), timedelta1)
    new_added = some_date5.__add__(timedelta1)
    print(new_added, some_date5, timedelta1)
    some_date5.__iadd__(timedelta1)
    print(some_date5)

