import pandas as pd
import psycopg2
from psycopg2 import Error

from WebApp.models import ConnectingToKIS
from . import string_snippets


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
            return f'SELECT concat_ws(\' \',m.surname,m.name,m.patron) AS ФИО_Пациента,' \
                f' concat_ws (\' - \',m.num,m.YEAR) AS №ИБ,' \
                f' mm.emp_get_fio_by_id (d.manager_emp_id ) AS Заведующий_отделением,' \
                f' to_char(tt.sign_dt,\'DD.MM.YYYY HH24:MM:SS \') AS Дата_подписи_леч_врачом,' \
                f' to_char (h.leave_dt,\'DD.MM.YYYY HH24:MM:SS\') AS Дата_выписки_пациента' \
                f' FROM mm.hospdoc h' \
                f' JOIN mm.mdoc m ON m.id = h.mdoc_id' \
                f' JOIN mm.people p ON p.id = m.people_id' \
                f' JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id' \
                f' LEFT JOIN mm.dept d ON d.id = h.dept_id' \
                f' JOIN (SELECT et.ehr_case_id, et.sign_dt,' \
                f' et.epic_code,' \
                f' et.creator_emp_id AS emp_id' \
                f' FROM mm.epic_text et' \
                f' WHERE  et.epic_code IN  (\'Z00.001.008\', \'Z00.001.012\', \'Z00.004.032\', \'Z00.001.014\', \'Z00.001.009\', \'Z00.001.016\')' \
                f' AND et.create_dt >= \'01.01.2023\'' \
                f' and et.allow_export = 2' \
                f' AND et.ehr_case_id NOT IN' \
                f' (SELECT hoer.ehr_case_id' \
                f' FROM mm.hospdoc_out_emiac_remd hoer' \
                f' WHERE hoer.create_dt >= \'01.01.2023\'' \
                f' AND hoer.status = 1)' \
                f' AND et.sign_dt NOTNULL) tt ON tt.ehr_case_id = h.ehr_case_id' \
                f' AND h.leave_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\'' \
                f' AND d.name = \'{self.dept}\''
        else:
            return f'SELECT' \
                f' concat_ws (\' \',p.surname,p.name,p.patron) AS Назначил,' \
                f' concat_ws (\' - \',m.num,m.YEAR) AS №ИБ,' \
                f' concat_ws(\' \',m.surname,m.name,m.patron) AS ФИО_Пациента,' \
                f' n.name AS Назначение,' \
                f' to_char(n.create_dt, \'DD.MM.YYYY HH24:MM:SS\') AS Создано,' \
                f' to_char(n.plan_dt, \'MM.YYYY HH24:MM:SS\'),' \
                f' CASE n.naz_extr_id ' \
                f'\tWHEN \'0\' THEN \'Планово\' ' \
                f'\tWHEN \'1\' THEN \'Экстренно\' ' \
                f' ELSE n.naz_extr_id::TEXT ' \
                f' END ' \
                f' FROM mm.mdoc AS m ' \
                f' JOIN mm.hospdoc h ON h.mdoc_id = m.id ' \
                f' JOIN mm.naz n ON n.mdoc_id = m.id ' \
                f' JOIN mm.emp AS em ON  em.id = n.creator_emp_id ' \
                f' JOIN mm.dept AS dp ON  dp.id = em.dept_id ' \
                f' JOIN mm.people AS p ON  p.id = em.people_id ' \
                f' JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id ' \
                f' LEFT JOIN mm.naz_action na  ON na.id = n.id ' \
                f' WHERE n.create_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\' ' \
                f' AND n.naz_view = \'{self.types_converting[self.research]}\'' \
                f' AND n.naz_state_id = 2 ' \
                f' AND dp.name = \'{self.dept}\''


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
    top_of_template = string_snippets.top_of_template
    bot_of_template = string_snippets.bot_of_template

    def __init__(self, db_data):
        self.db_data = db_data

    def output_data(self, error_value=None):
        """ Prepare raw data getting from KIS DB and creating HTML template based on them. Data handled by PANDAS. """
        if error_value:
            # Date validations error text instead data table
            tab = string_snippets.date_validation_error
            # Editing strings of html template
            ReadyReportHTML.top_of_template = ReadyReportHTML.top_of_template \
                .replace('<br><br>Невыполненные {{chosen_type}} за перод с {{from_dt}} по {{to_dt}}', '')
        else:
            if type(self.db_data) is list and len(self.db_data) == 0:
                tab = string_snippets.tab_done
            elif type(self.db_data) is list and len(self.db_data) != 0:
                row_values = len(self.db_data[0])
                rows_number = len(self.db_data)
                # DataFrame's headers names for all type of researches
                headers_names = ['Врач', 'Номер ИБ', 'Пациент', 'Назначение',
                                 'Дата создания', 'Назначено на дату', 'Статус']
                # 5 values in 1 row - if user chosen "Невыгруженные эпикризы"
                if row_values == 5:
                    headers_names = ['ФИО пациента', 'ИБ пациента', 'Заведующий отделения',
                                     'дата подписи выписного эпикриза', 'Дата выписки пациента']
                # List of lists of data separated and grouped inside
                data_lists = [list(map(lambda x: x[i], self.db_data)) for i in range(row_values)]
                # Creating dict for DataFrame
                data = dict(zip(headers_names, data_lists))
                df = pd.DataFrame(data=data, index=range(1, rows_number+1))
                string_snippets.top_of_template.replace('\t\t<div class="table-container">\n',
                                                        '\t\t<p class="center-top-text">Количество невыполненных назначений: {{ common_rows_number }}</p>\n\t\t<div class="table-container">\n')
                # Converting to HTML block inside the <table> tag
                # It is middle part of body of the HTML template
                tab = df.to_html()
            elif type(self.db_data) is str:
                tab = f'\t<p class="center-top-text">{self.db_data}</p>\n'
            else:
                tab = string_snippets.system_error
        # Updating template by overwriting when get the new data from KIS
        with open(r'C:\Users\adm-ryadovoyaa\Documents\DMKprojects\MedVeiws\observer\WebApp\templates\output.html', 'wt',
                  encoding='utf-8') as template:
            template.write(ReadyReportHTML.top_of_template)
            template.writelines(tab)
            template.writelines(ReadyReportHTML.bot_of_template)
