from typing import Any
from datetime import date
import calendar

key_months = [i for i in range(1, 13)]
val_months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля',
              'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
months = dict(zip(key_months, val_months))


def date_converter(date_srting: str) -> str:
    """ Reversing date string to improve readability for users
    and changing months number to string on RU language.

    arguments:
    date_srting -- date object in string format (result of date_pg_format function)
    """
    prep = date_srting.split('-')
    month = months[int(prep[1])]
    ready_date = f'{prep[2]}  {month}  {prep[0]}'
    return ready_date


def date_pg_format(func: Any) -> list:
    """ Getting values from response and creating list containing date - both from and to
    (in from keys requesting order).

    func -- django function for get info from web response.
    """
    request_keys = ['from_dt_year', 'from_dt_month', 'from_dt_day', 'to_dt_year', 'to_dt_month', 'to_dt_day']
    dates_values = [func(i) for i in request_keys]
    return dates_values


def chosen_date(date_string) -> Any:
    """
    Describing
    """
    raw_values = [int(i) for i in date_string.split('-')]
    ready_date = date(year=raw_values[0], month=raw_values[1], day=raw_values[2])
    return ready_date


def calendar_create() -> str:
    today = date.today()
    # Get the day of the week for today's date (0 = Monday, 6 = Sunday)
    web_calendar = calendar.LocaleHTMLCalendar().formatmonth(theyear=today.year,
                                                             themonth=today.month,
                                                             withyear=True)
    web_calendar = web_calendar.replace(f'<td class="sat">{today.day}</td>',
                                        f'<td class="sat today" id="today">{today.day}</td>', 1)
    return web_calendar


class FrontDataValues:
    """ Describing list containing 10 values only. Values adding
    into list from api_func.
    """
    val_list = []

    def __init__(self, value):
        self.value = value

    def adding(self) -> Any:
        """
        Adding gotten value from frontend to class
         attribute list for further handling.
        """
        if len(self.val_list) == 2:
            self.val_list.clear()
        self.val_list.append(self.value)
        return self.val_list
