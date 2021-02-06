from typing import Optional, overload


class TimeDelta:
    def __init__(self, days: Optional[int] = None, months: Optional[int] = None, years: Optional[int] = None):
        ...


class Date:
    """Класс для работы с датами"""

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
                self._day = int(values[0])
                self.month = int(values[1])
                self._year = int(values[2])
        elif len(args) == 3:
            self._day = args[0]
            self._month = args[1]
            self._year = args[2]
        else:
            raise ValueError("Incorrect date format")

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        return str(f'{self._day}.{self._month}.{self._year}')

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""

    def is_leap_year(self, year: int) -> bool:
        """Проверяет, является ли год високосным"""

    def get_max_day(self, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""

    def is_valid_date(self, day: int, month: int, year: int):
        """Проверяет, является ли дата корректной"""

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """value от 1 до 31. Проверять значение и корректность даты"""
        self._day = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """value от 1 до 12. Проверять значение и корректность даты"""
        self._month = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """value от 1 до ... . Проверять значение и корректность даты"""
        self._year = value

    def __sub__(self, other: "Date") -> int:
        """Разница между датой self и other (-)"""

    def __add__(self, other: TimeDelta) -> "Date":
        """Складывает self и некий timedeltа. Возвращает НОВЫЙ инстанс Date, self не меняет (+)"""

    def __iadd__(self, other: TimeDelta) -> "Date":
        """Добавляет к self некий timedelta меняя сам self (+=)"""


if __name__ == '__main__':
    some_date1 = Date(30, 3, 3333)
    print(some_date1.day, some_date1.month, some_date1.year, some_date1)
    some_date2 = Date('12.12.1222')
    print(some_date2.day, some_date2.month, some_date2.year)
    some_date3 = Date('12.12')
    print(some_date3.day, some_date3.month, some_date3.year)
    print("Hello")