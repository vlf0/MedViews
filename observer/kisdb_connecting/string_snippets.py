top_of_template = (
        '<!DOCTYPE html>\n'
        '<html lang="ru">\n'
        '<head>\n'
        '\t{% load static %}\n'
        '\t<link rel="stylesheet" type="text/css" href="{% static \'index.css\' %}">\n'
        '\t<meta charset="UTF-8">\n'
        '\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '\t<link rel="shortcut icon" type="image/png" href="{% static \'favicon.ico\' %}">\n'
        '\t<title>Second Page</title>\n'
        '\t</head>\n\n'
        '<body>\n'
        '\t\t<p class="center-top-text">Отделение: {{ chosen_dept }}<br><br>\n'
        '\t\t\tЗаведущий: {{ doc }}<br><br>Невыполненные {{chosen_type}} за перод с {{from_dt}} по {{to_dt}}</p>\n'
        '\t<div class="container">\n'
        '\t<form action="{% url \'output\' chosen_dept chosen_type \'from_dt\' \'to_dt\' %}" method="POST">\n'
        '\t<table>\n'
        '\t\t{{ types_list }}\n'
        '\t\t{{ date_buttons }}\n'
        '\t</table>\n'
        '\t\t<div class="button-container">\n'
        '\t\t\t<button type="submit" class="common_button"> <b>Построить отчет</b> </button>\n'
        '\t\t</div>\n'
        '\t{% csrf_token %}\n'
        '\t\t</form>\n'
        '\t<form action="{% url \'dept\' %}" method="GET">\n'
        '\t\t<div class="button-container">\n'
        '\t\t\t<button type="submit" class="common_button"> <b>Вернуться к выбору отделений</b> </button>\n'
        '\t\t</div>\n'
        '\t</form>\n'
        '\t\t<div class="table-container">\n'
    )

bot_of_template = (
        '\n\t\t</div>\n'
        '\n\t</div>\n'
        '</body>\n'
        '</html>'
)

tab_done = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n'

tab_report = '\t\t<p class="center-top-text">Количество невыполненных назначений: {{ common_rows_number }}</p>\n'

system_error = '\t<p class="center-top-text">SYSTEM ERROR!</p>\n'

date_validation_error = '\t\t<p class="center-top-text">Дата окончания периода не может быть меньше даты начала!</p>\n'

depts_list = 'SELECT name FROM mm.dept d' \
             ' WHERE name in (\'ПО\', \'Терапия\')'

