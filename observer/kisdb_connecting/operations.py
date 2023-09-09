import pandas as pd
import psycopg2
from psycopg2 import Error

from WebApp.models import ConnectingToKIS


class Queries:
    """ This object consists of gotten values from web pages
     and returns full query in string format ready to use in DB. """
    def __init__(self, dept, research, from_dt, to_dt):
        self.dept = dept
        self.research = research
        self.from_dt = from_dt
        self.to_dt = to_dt

    def ready_select(self):
        return f'SELECT * FROM mm.dbkis WHERE dept = \'{self.dept}\' AND status = \'{self.research}\' ' \
               f'AND create_dt between \'{self.from_dt}\' and \'{self.to_dt}\''


class SelectAnswer:
    """ Represent SQL query object in the text format. """
    def __init__(self, query_text):
        self.query_text = query_text

    def selecting(self):
        """ Connecting to DB and execute SQL query. If connect not established or
        bad query getting - throw exceptions that displaying on the web page. """
        if len(ConnectingToKIS.objects.all()) != 0:
            for conn_data in ConnectingToKIS.objects.all():
                if conn_data.active is True:
                    try:
                        connection = psycopg2.connect(database='postgres',
                                                      host='localhost',
                                                      port='5432',
                                                      user='postgres',
                                                      password='root')
                        try:
                            cursor = connection.cursor()
                            cursor.execute(self.query_text)
                            selecting_data = cursor.fetchall()
                            return selecting_data
                        except (Exception, Error):
                            return 'Connect to DB = SUCCSESS.\nError in SQL query!\nCall to admin!'
                        finally:
                            cursor.close()
                            connection.close()
                    except (Exception, Error):
                        return 'Can not connect to BD!\nCall to admin!'
                    # finally:
                        # try:
                        #     if connection:
                        #         cursor.close()
                        #         connection.close()
                        # except UnboundLocalError:
                        #     pass
                else:
                    return 'DB not active!\n To use it - turn on check box in the admin panel!'
        else:
            return 'There are no any records in the BD data tab!'


class ReadyReportHTML:
    """ Represent HTML page and contains selected required data.
    The data converts to HTML code by Pandas DataFrame. Data for connecting get from app DB models. """
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
        '\t<form action="{% url \'output\' chosen_dept \'chosen_type\' \'from_dt\' \'to_dt\' %}" method="POST">\n'
        '\t<table>\n'
        '\t\t{{ types_list }}\n'
        '\t\t{{ date_buttons }}\n'
        '\t</table>'
        '\t\t<button type="submit" id="ref"> <b>Выбрать</b> </button>\n'
        '\t{% csrf_token %}\n'
        '\t\t</form>\n'

        '\t<form action="{% url \'dept\' %}" method="GET">\n'
        '\t\t<button type="submit" id="gt"> <b>Вернуться к выбору отделений</b> </button>\n'
        '\t</form>\n'
    )

    bot_of_template = (
        '\n\t</div>\n'
        '</body>\n'
        '</html>'
    )

    def __init__(self, db_data):
        self.db_data = db_data

    def output_data(self):
        """ Prepare raw data getting from KIS DB and creating HTML template based on them. Data handled by PANDAS. """
        if type(self.db_data) is list and len(self.db_data) == 0:
            tab = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n'
        elif type(self.db_data) is list and len(self.db_data) != 0:
            # # List of lists that will be DataFrame dict values
            data_lists = []
            for i in self.db_data[0]:
                data_lists.append([])
            # Raw list iterations from KIS DB
            # Then iteration of separated record from list represented in the tuple
            for record in self.db_data:
                list_key_index = 0
                for row in record:
                    data_lists[list_key_index].append(row)
                    list_key_index += 1
            # # print(data_lists)
            # Data dict - argument to the DataFrame
            dict_key_index = 0
            data = {
                    'fio_doc': [],
                    'ib_num': [],
                    'pat_fio': [],
                    'research': [],
                    'create_dt': [],
                    'status': [],
                    'dept': [],
                    'plan_dt': []
                    }
            # Values assignment to data keys
            for i in data:
                data[i] = data_lists[dict_key_index]
                dict_key_index += 1
            # # print(data)
            df = pd.DataFrame(data=data)
            # Converting to HTML block in the <table> tag
            # It is middle part of body of the HTML template
            tab = df.to_html()
        elif type(self.db_data) is str:
            tab = f'\t<p class="center-top-text">{self.db_data}</p>\n'
        else:
            tab = '\t<p class="center-top-text">SYSTEM ERROR!</p>\n'
        # Updating template by overwriting when get the new data from KIS
        with open(r'D:\Programming\DjangoProjects\MedVeiws\observer\WebApp\templates\output.html', 'wt',
                  encoding='utf-8') as template:
            template.write(ReadyReportHTML.top_of_template)
            template.writelines(tab)
            template.writelines(ReadyReportHTML.bot_of_template)
