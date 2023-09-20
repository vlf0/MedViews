from typing import Any
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        """ Adding gotten value from frontend to class
        attribute list for further handling.
        """
        if len(self.val_list) == 2:
            self.val_list.clear()
        self.val_list.append(self.value)
        return self.val_list


def validate_dates(first_date, second_date):
    """ Do checking if second date value inserting
    by user not less than first value.
    """
    first = first_date.split('-')
    first = list(map(lambda x: int(x), first))
    first_value = datetime(year=first[0], month=first[1], day=first[2],).timestamp()

    second = second_date.split('-')
    second = list(map(lambda x: int(x), second))
    second_value = datetime(year=second[0], month=second[1], day=second[2]).timestamp()
    if first_value > second_value:
        return False
    else:
        return True
