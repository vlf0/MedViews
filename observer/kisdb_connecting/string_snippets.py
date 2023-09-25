top_of_template = (
        '<!DOCTYPE html>\n'
        '<html lang="ru">\n'
        '<head>\n'
        '\t{% load static %}\n'
        '\t<link rel="stylesheet" type="text/css" href="{% static \'index.css\' %}">\n'
        '\t<meta charset="UTF-8">\n'
        '\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '\t<link rel="shortcut icon" type="image/png" href="{% static \'GKB_D_sign.ico\' %}">\n'
        '\t<title>Second Page</title>\n'
        '\t</head>\n\n'
        '<body>\n'
        '\t<div class="logo">\n'
        '\t<img src="{% static \'gkblogo.png\' %}" alt="logo">\n'
        '\t</div>\n'
        '\t\t<p class="center-top-text">Отделение: {{ chosen_dept }}<br><br>\n'
        '\t\t\tЗаведущий: {{ doc }}<br><br>Невыполненные {{chosen_type}} за перод с {{from_dt}} по {{to_dt}}</p>\n'
        '\t<div class="container"\n>'
        '\t\t<form id="create_report" action="{% url \'output\' chosen_dept'
        ' chosen_type \'from_dt\' \'to_dt\' %}" method="POST"\n>'
        '\t\t\t<table>\n'
        '\t\t\t\t{{ types_list }}\n'
        '\t\t\t\t{{ date_buttons }}\n'
        '\t\t\t\t{% csrf_token %}\n'
        '\t\t\t</table>\n'
        '\t\t</form>\n'
        '\t</div>\n'
        '\t\t<form id="dept_choice" action="{% url \'dept\' %}" method="GET"></form>\n'
        '\t<div class="button-container">\n'
        '\t\t<button form="create_report" type="submit" class="common_button"> <b>Построить отчет</b> </button>\n'
        '\t</div>\n'
        '\t<div class="button-container">\n'
        '\t\t<button form="dept_choice" type="submit" class="common_button"> <b>Вернуться к выбору отделений</b> </button>\n'
        '\t</div>\n'
    )

bot_of_template = (
        '</body>\n'
        '</html>'
)

tab_table = '\t<div class="table-container">\n'

tab_table_end = '\n\t\t</div>\n'

tab_done = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n'

tab_report = '\t\t<p class="center-top-text">Количество невыполненных назначений: {{ common_rows_number }}</p>\n'

system_error = '\t<p class="center-top-text">SYSTEM ERROR!</p>\n'

date_validation_error = '\t\t<p class="center-top-text">Дата окончания периода не может быть меньше даты начала!</p>\n'

depts_by_ids = 'SELECT d.name FROM mm.dept d'
