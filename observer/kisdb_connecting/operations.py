import pandas as pd
import psycopg2
from psycopg2 import Error


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
    '\t<div class="container">\n'
    '\t  <p class="center-top-text">Выберите отделение и нажмите кнопку "далее"</p>\n'
    '\t<form action="{% url \'output\' chosen_dept \'chosen_type\' %}" method="POST">\n'
    '\t<table>\n'
    '\t\t{{ types_list }}\n'
    '\t</table>'
    '\t\t<button type="submit" id="ref" > <b>Выбрать</b> </button>\n'
    '\t                      {% csrf_token %}\n'
    '\t</form>\n'
)



bot_of_template = (
    '\n\t</div>\n'
    '</body>\n'
    '</html>)'
)


def select_query(research_type, status):
    # selecting_query = f'SELECT * FROM mm.cons2 WHERE status = \'{research_type}\''
    selecting_query = f'SELECT * FROM mm.{research_type} WHERE status = \'{status}\''
    return selecting_query


def connecting(sql_query):
    """ Simple connecting to DB and getting data. """
    # try:
    # # Connect to needed DB
    connection = psycopg2.connect(database='postgres', host='localhost',
                                  port='5432', user='postgres', password='root')
    cursor = connection.cursor()
    # Executing query and getting list of rows represented in tuples
    cursor.execute(sql_query)
    selecting_data = cursor.fetchall()
    # print(len(selecting_data))
    return selecting_data

    # # Caught all possible exceptions
    # except (Exception, Error) as error:
    #     return 'Bad SQL request or another DB problem. Call to administrator.'
    # finally:
    #     try:
    #         if connection:
    #             cursor.close()
    #             connection.close()
    #     except UnboundLocalError:
    #         return False



def preparing_data(db_data):
    """ Prepare raw data getting from KIS DB and creating HTML template based on them. """
    if type(db_data) is list and len(db_data) == 0:
        tab = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n'
    elif type(db_data) is list and len(db_data) != 0:
        # List of lists that will be DataFrame dict values
        data_lists = [id := [], fio := [], doc_num := [], research := [], add_data := [],
                      plan_data := [], status := [], research_type := []]

        # Raw list iterations from KIS DB
        # Then iteration of separated record from list represented in the tuple
        for record in db_data:
            for row in record:
                data_lists[record.index(row)].append(row)

        key_index = 0
        # Data dict - argument to the DataFrame
        data = {'id': [],
                'fio_doc': [],
                'doc_num': [],
                'pat_fio': [],
                'naz_type': [],
                'add_data': [],
                'plan_data': [],
                'status': []
                }
        # Values assignment to data keys
        for i in data:
            data[i] = data_lists[key_index]
            key_index += 1
        # print(data)
        df = pd.DataFrame(data=data)
        # Converting to HTML block in the <table> tag
        # It is middle part of body of the HTML template
        tab = df.to_html()
    elif type(db_data) is str:
        tab = f'\t<p class="center-top-text">{db_data}</p>\n'
    else:
        tab = '\t<p class="center-top-text">ОШИБКА РАБОТЫ С БД. Обратитесть к администратору.</p>\n'
    # Updating template by overwriting when get the new data from KIS
    with open(r'D:\Programming\DjangoProjects\MedVeiws\observer\WebApp\templates\output.html', 'wt',
              encoding='utf-8') as template:
        template.write(top_of_template)
        template.writelines(tab)
        template.writelines(bot_of_template)

# print(preparing_data(connecting(f'SELECT * FROM mm.cons2 WHERE status = \'Назначено\'')))