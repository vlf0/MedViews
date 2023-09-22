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
        '\t<div class="button-container">\n'
        '\t\t<button form="create_report" type="submit" class="common_button"> <b>Построить отчет</b> </button>\n'
        
        '\t\t<form action="{% url \'dept\' %}" method="GET">\n'
        '\t\t<button type="submit" class="common_button"> <b>Вернуться к выбору отделений</b> </button>\n'
        '\t\t</form>\n'
        '\t</div>\n'
        '\t<div class="table-container">\n'
    )

bot_of_template = (
        '\n\t\t</div>\n'
        '\n\t</div>\n'
        '</body>\n'
        '</html>'
)

tab_done = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n'

# tab_report = '\t\t<p class="center-top-text">Количество невыполненных назначений: {{ common_rows_number }}</p>\n'

system_error = '\t<p class="center-top-text">SYSTEM ERROR!</p>\n'

date_validation_error = '\t\t<p class="center-top-text">Дата окончания периода не может быть меньше даты начала!</p>\n'

depts_by_ids = 'SELECT d.name FROM mm.dept d' \
              ' WHERE d.id IN' \
              ' (\'b99a5265-74c0-4ace-8cb3-1fe204b59aaf\',\'faf07796-1ffb-478e-a06e-717dfc46a7ec\',' \
              ' \'1662afce-46b5-44f7-bec2-0379045f7224\', \'1fb01ccf-64b2-4fe5-b914-9c5eca23e120\',' \
              ' \'495f76bb-0bf2-4384-acc0-0e1bdc3b7016\', \'51cf4e23-36e7-4ac8-9d93-1d31a7c2b9a2\',' \
              ' \'7215749c-9511-46b4-b45f-2d06ea968402\', \'958fe9e3-06e8-4a61-aaa5-7839eb91a2c5\',' \
              ' \'1d8cf85a-38b1-4220-b6b0-bdc93a32da02\', \'cad1687b-74cb-4181-833c-b8487cb3c1a2\',' \
              ' \'84db1d24-186d-4352-93ce-fe55391da7d4\', \'bf7fd4e9-f743-4ce5-86b5-fe2f8edf6a39\',' \
              ' \'1a368a46-9c40-4c7b-a260-01bce04ece7e\', \'52c623a6-d1c4-48ed-8644-3f7b68d78e88\',' \
              ' \'99e772e8-ed16-4da5-a6db-aaee05bc4e66\', \'bb26d215-d705-4751-8665-a4249cc1a7a6\',' \
              ' \'ce8a8f10-2dab-447d-b4d3-fc75939feb52\', \'ef12e48a-55d4-45fe-a448-cd7ded5eba42\',' \
              ' \'2577fa8a-9440-46b8-805c-bb47be7f452c\', \'0f49d6a5-19c7-466a-b30a-314d2ab0c222\',' \
              ' \'7f35c044-8375-4057-8d04-bba5573b4f85\', \'dc3ec9ee-a75c-45ab-9672-241e7618733a\',' \
              ' \'863d276b-abe3-4b50-a920-6901292d70f0\', \'b3046a27-2ed1-4cb7-8150-e70f68e75810\',' \
              ' \'5fe0204b-e340-486a-94db-2bcc75fc6e64\', \'7168f375-ac21-4c66-9575-f033c3ac0cd3\','\
              ' \'85489221-1971-4a7a-9878-52ea814769ee\')'