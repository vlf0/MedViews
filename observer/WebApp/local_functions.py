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


# def calendar_create() -> Any:
#     today = date.today()
#     web_calendar = calendar.HTMLCalendar().formatmonth(theyear=today.year,
#                                                        themonth=today.month,
#                                                        withyear=True)
#     print(web_calendar)
#     web_calendar = web_calendar.replace(f'class="sat">', 'class="sat today">')
#     return web_calendar
#
#
# print(calendar_create())

def calendar_create() -> str:
    today = date.today()
    # Get the day of the week for today's date (0 = Monday, 6 = Sunday)
    day_of_week = date(today.year, today.month, today.day).weekday()
    cal = calendar.HTMLCalendar().formatmonth(today.year, today.month, withyear=True)
    # Replace the class attribute for the cell corresponding to today's date
    cal = cal.replace(f'<td class="sat">{today.day}</td>', f'<td class="sat today">{today.day}</td>', 1)

    return cal

