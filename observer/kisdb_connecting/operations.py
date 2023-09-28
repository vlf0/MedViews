import re
import pandas as pd
import psycopg2
from psycopg2 import Error
from datetime import date, datetime, timedelta
from WebApp.models import ConnectingToKIS
from . import string_snippets


today = datetime.today()
three_days = timedelta(days=3, hours=0, minutes=0, microseconds=0, milliseconds=0)


class Queries:
    """ This object consists of gotten values from web pages
     and returns full query in string format ready to use in DB. """
    types_converting = {
        'Лабораторные исследования': 1,
        'Инструментальные исследования': 2,
        'Процедуры и манипуляции': 3,
        'Операции': 4,
        'Консультации': 5,
        'Невыгруженные эпикризы': 7
    }

    def __init__(self, dept, research, from_dt, to_dt):
        self.dept = dept
        self.research = research
        self.from_dt = from_dt
        self.to_dt = to_dt

    def ready_select(self):
        if self.types_converting[self.research] == 7:
            return f'SELECT pat_fio, pat_ib, zav, sign_dt, pat_leave_dt FROM mm.tap' \
                   f' WHERE sign_dt between \'{self.from_dt}\' and \'{self.to_dt}\''
        else:
            return f'select doc_fio, ib_num, pat_fio, research, create_dt, plan_dt FROM mm.dbkis' \
                   f' WHERE dept = \'{self.dept}\' AND r_type = \'{self.types_converting[self.research]}\'' \
                   f' AND create_dt between \'{self.from_dt}\' and \'{self.to_dt}\''


class SelectAnswer:
    """ Represent SQL query object in the text format. """
    def __init__(self, query_text):
        self.query_text = query_text

    def selecting(self):
        """ Connecting to DB and execute SQL query. If connect not established or
        bad query getting - throw exceptions that displaying on the web page. """
        if len(ConnectingToKIS.objects.all()) != 0:
            actual_db = ConnectingToKIS.objects.filter(active='True').values()
            if len(actual_db) == 1:
                actual_db = actual_db[0]
                try:
                    connection = psycopg2.connect(database=actual_db['db'],
                                                  host=actual_db['host'],
                                                  #   port=5431,
                                                  port=actual_db['port'],
                                                  user=actual_db['user'],
                                                  password=actual_db['password'])
                    try:
                        cursor = connection.cursor()
                        cursor.execute(self.query_text)
                        selecting_data = cursor.fetchall()
                        return selecting_data
                    except (Exception, Error) as e:
                        return f'Error!\n\n{e}\n'
                    finally:
                        cursor.close()
                        connection.close()
                except (Exception, Error) as e:
                    print(e)
                    return f'Error!\n\n{e}\n'
            elif len(actual_db) > 1:
                return 'There are more than one DataBases in ACTIVE status!\n' \
                       ' Check DB in active in the admin panel!'
            else:
                return 'DB not active!\n To use it - turn on check box in the admin panel!'
        else:
            return 'There are no any records in the BD data tab!'


class ReadyReportHTML:
    """ Represent HTML page and contains selected required data.
    The data converts to HTML code by Pandas DataFrame. Data for connecting get from app DB models. """
    def __init__(self, db_data):
        self.db_data = db_data

    def output_data(self, error_value=None):
        """ Prepare raw data getting from KIS DB and creating HTML template based on them. Data handled by PANDAS. """
        if error_value:
            # Date validations error text instead data table
            tab = string_snippets.date_validation_error
            # Editing strings of html template
            string_snippets.top_of_template = string_snippets.top_of_template\
                .replace('<br><br>Невыполненные {{chosen_type}} за перод с {{from_dt}} по {{to_dt}}', '')
        else:
            if type(self.db_data) is list and len(self.db_data) == 0:
                tab = string_snippets.tab_done
            elif type(self.db_data) is list and len(self.db_data) != 0:
                row_values = len(self.db_data[0])
                rows_number = len(self.db_data)
                # List of lists of data separated and grouped inside
                data_lists = [list(map(lambda x: x[i], self.db_data)) for i in range(row_values)]
                # DataFrame's headers names for all type of researches
                headers_names = ['Врач', 'Номер ИБ', 'Пациент', 'Назначение',
                                 'Дата создания', 'Назначено на дату', 'Статус']

                # 5 values in 1 row - if user chosen "Невыгруженные эпикризы"
                if row_values == 5:
                    headers_names = ['ID', 'ФИО пациента', 'ИБ пациента', 'Заведующий отделения',
                                     'Дата подписи выписного эпикриза', 'Дата выписки пациента']
                    # Adding list of row numbers into begin headers_names (creating own column of indexes)
                    data_lists.insert(0, [i for i in range(1, rows_number+1)])
                # Creating dict for DataFrame
                data = dict(zip(headers_names, data_lists))
                df = pd.DataFrame(data=data, index=range(1, rows_number+1))
                second_column_name = df.head(0).columns.values[1]
                # Converting to HTML block inside the <table> tag
                # It is middle part of body of the HTML template
                if second_column_name == 'ФИО пациента':
                    df.insert(loc=6, column='Не выгружено (кол-во дней)',
                              value=(today - df['Дата подписи выписного эпикриза'].array).days)
                    # Applying format to cells by condition
                    report = df.to_html(formatters={
                                        'ID': lambda x: f'over{x}'
                                        if (today - df.at[x, 'Дата подписи выписного эпикриза'])
                                        > three_days else f'{x}'
                                        }, justify='center', index=False)
                    # Changing color and style in the all ID's cells
                    report = re.sub(r'<tr>\s*<td>', '<tr>\n\t  <td bgcolor="#be875c" style="text-align: center;">',
                                    report)
                    # Applying entire row color style where is text "over" (it is condition for dates comparison)
                    report = re.sub(r'<tr>\s*<td bgcolor="#be875c" style="text-align: center;">over',
                                    '<tr bgcolor="yellow">\n\t  <td bgcolor="#be875c" style="text-align: center;">',
                                    report)
                else:
                    df.columns.rename('ID', inplace=True)
                    report = df.to_html(justify="center")
                    # Adding own class for further applying css for column "ID"
                    report = re.sub(r'<tr style="text-align: center;">\s*<th>ID',
                                    '<tr style="text-align: center;">\n\t  <th class="index-name">ID', report)
                # Result of creating dataframe and formatting to HTML
                tab = string_snippets.tab_report + string_snippets.tab_table + report + string_snippets.tab_table_end

            elif type(self.db_data) is str:
                tab = f'\t<p class="center-top-text">{self.db_data}</p>\n'
            else:
                tab = string_snippets.system_error
        # Updating template by overwriting when get the new data from KIS
        with open(r'D:\Programming\DjangoProjects\MedVeiws\observer\WebApp\templates\output.html', 'wt',
                  encoding='utf-8') as template:
            template.write(string_snippets.top_of_template)
            template.writelines(tab)
            template.writelines(string_snippets.bot_of_template)
