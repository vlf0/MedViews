from datetime import datetime


key_months = [i for i in range(1, 13)]
val_months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля',
              'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
months = dict(zip(key_months, val_months))


def date_converter(date_string: str) -> str:
    """ Reversing date string to improve readability for users
    and changing months number to string on RU language.

    arguments:
    date_string -- date object in string format (result of date_pg_format function)
    """
    prep = date_string.split('-')
    month = months[int(prep[1])]
    ready_date = f'{prep[2]}  {month}  {prep[0]}'
    return ready_date


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
