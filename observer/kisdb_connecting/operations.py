import re
import pandas as pd
import psycopg2
import pathlib
from psycopg2 import Error
from datetime import datetime, timedelta
from WebApp.models import ConnectingToKIS
from . import string_snippets


today = datetime.today()
three_days = timedelta(days=3, hours=0, minutes=0, microseconds=0, milliseconds=0)


def dates(x):
    x = datetime.strftime(x, '%d.%m.%Y %H:%M:%S')
    dt, tm = x.split(' ')
    result = '-'.join(dt.split('-')[::-1]) + ' ' + str(tm)
    return result


def overstay(x):
    if x in list(range(11, 21)) or (x not in [1, 2, 3, 4] and str(x)[-1] not in ['1', '2', '3', '4']):
        x = f'Center {x} дней'
    elif str(x)[-1] == '1':
        x = f'Center {x} день'
    elif x in [2, 3, 4] or str(x)[-1] in ['2', '3', '4'] and x not in list(range(11, 21)):
        x = f'Center {x} дня'
    if int(x.split(' ')[1]) > 3:
        x = f'Over{x}'
    return x


def style_and_remove_overcenter(row):
    if 'OverCenter' in row:
        # Remove 'OverCenter' text and apply background color
        styled_row = re.sub(r'<td>OverCenter', '<td style="text-align: center;">', row)
        return f'<tr style="background-color: #FFCCCB;">{styled_row}</tr>'
    return f'<tr>{row}</tr>'


class ReportExcelWriter:
    """ Applying styles to dataframe going to excel file.
    Has two methods for two different reports. """
    @staticmethod
    def xlsx_styles_researches(dept_name, frame):
        writer = pd.ExcelWriter(f'./WebApp/static/reports/rep_{dept_name}.xlsx', engine='xlsxwriter')
        frame.to_excel(excel_writer=writer, sheet_name='Отчёт', engine='xlsxwriter', index=False)
        writer.sheets['Отчёт'].set_column(0, 0, 45)
        writer.sheets['Отчёт'].set_column(1, 1, 10)
        writer.sheets['Отчёт'].set_column(2, 3, 45)
        writer.sheets['Отчёт'].set_column(4, 5, 22)
        writer.sheets['Отчёт'].set_column(6, 6, 10)
        writer.close()

    @staticmethod
    def xlsx_styles_epicrisis(dept_name, frame):
        writer = pd.ExcelWriter(f'./WebApp/static/reports/rep_{dept_name}.xlsx', engine='xlsxwriter')
        frame.to_excel(excel_writer=writer, sheet_name='Отчёт', engine='xlsxwriter', index=False)
        writer.sheets['Отчёт'].set_column(0, 0, 5)
        writer.sheets['Отчёт'].set_column(1, 1, 45)
        writer.sheets['Отчёт'].set_column(2, 2, 10)
        writer.sheets['Отчёт'].set_column(3, 3, 45)
        writer.sheets['Отчёт'].set_column(4, 5, 20)
        writer.sheets['Отчёт'].set_column(6, 6, 5)
        writer.close()


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
            return f'SELECT' \
                f' mm.famaly_io(p.surname,p.name,p.patron) AS ФИО_Пациента,' \
                f' concat_ws (\' - \',m.num,m.YEAR) AS №ИБ,' \
                f' mm.emp_get_fio_by_id (h.doctor_emp_id ) AS Лечащий_врач,' \
                f' tt.sign_dt AS Дата_подписи_леч_врачом,' \
                f' h.leave_dt AS Дата_выписки_пациента' \
                f' FROM mm.hospdoc h' \
                f' JOIN mm.mdoc m ON m.id = h.mdoc_id' \
                f' JOIN mm.people p ON p.id = m.people_id' \
                f' JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id' \
                f' LEFT JOIN mm.dept d ON d.id = h.dept_id' \
                f' JOIN (SELECT et.ehr_case_id, et.sign_dt,' \
                f' et.epic_code,' \
                f' et.creator_emp_id AS emp_id' \
                f' FROM mm.epic_text et' \
                f' WHERE et.epic_code IN  (\'Z00.001.008\', \'Z00.001.012\', \'Z00.004.032\', \'Z00.001.014\', \'Z00.001.009\', \'Z00.001.016\')' \
                f' AND et.create_dt >= \'01.01.2023\'' \
                f' and et.allow_export = 2' \
                f' AND et.ehr_case_id NOT IN' \
                f' (SELECT hoer.ehr_case_id' \
                f' FROM mm.hospdoc_out_emiac_remd hoer' \
                f' WHERE hoer.create_dt >= \'01.01.2023\'' \
                f' AND hoer.status = 1)' \
                f' AND et.sign_dt NOTNULL) tt ON tt.ehr_case_id = h.ehr_case_id' \
                f' AND h.leave_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\'' \
                f' AND d.name = \'{self.dept}\'' \
                f' ORDER BY h.leave_dt ASC' 
        elif self.dept =='Приемное отделение':
            return f'SELECT' \
            f' n.creator_emp_fio AS Назначил,' \
            f' concat_ws (\'-\',md.num,md.YEAR,md.num_type) AS №ИБ,' \
            f' mm.famaly_io (p.surname,p.name,p.patron) AS ФИО_Пациента,' \
            f' n.name AS Назначение,' \
            f' n.create_dt AS создано,' \
            f' n.plan_dt AS Назначено_на_дату,' \
            f' CASE n.naz_extr_id' \
            f' \tWHEN \'0\' THEN \'Планово\' '\
            f' \tWHEN \'1\' THEN \'Экстренно\' '\
            f' ELSE n.naz_extr_id::TEXT ' \
            f' END AS Срочность' \
            f' FROM mm.naz n' \
            f' JOIN mm.naz_type nt ON nt.id = n.naz_type_id' \
            f' JOIN mm.naz_action na ON na."id" = n.last_action_id' \
            f' JOIN mm.naz_type_dir ntd on ntd.id = nt.naz_type_dir_id' \
            f' JOIN mm.ambticket a on a.mdoc_id = n.mdoc_id' \
            f' JOIN mm.hosp_refuse hr on hr.ambticket_id = a.id' \
            f' JOIN mm.emp ce ON ce.id = n.creator_emp_id' \
            f' JOIN mm.dept cd ON cd.id = ce.dept_id' \
            f' JOIN mm.mdoc md ON md.id = n.mdoc_id' \
            f' JOIN mm.mdoc_type mt on md.mdoc_type_id = mt.id' \
            f' JOIN mm.people p ON p.id = md.people_id' \
            f' WHERE n.naz_view = \'{self.types_converting[self.research]}\'' \
            f' AND n.create_dt between hr.input_dt and hr.end_dt' \
            f' AND hr.end_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\' ' \
            f' AND na.state_value not in (\'cancelled\', \'postponed\', \'completed\')' \
            f' AND cd.name = \'{self.dept}\''
        else:
            return f'SELECT' \
            f' concat_ws (\' \',p.surname,p.name,p.patron) AS Назначил,'\
            f' concat_ws (\' - \',m.num,m.YEAR) AS №ИБ,' \
            f' mm.famaly_io(m.surname,m.name,m.patron) AS ФИО_Пациента,' \
            f' n.name,' \
            f' n.create_dt AS создано,' \
            f' n.plan_dt AS Назначено_на_дату,' \
            f' CASE n.naz_extr_id ' \
            f'\tWHEN \'0\' THEN \'Планово\' ' \
            f'\tWHEN \'1\' THEN \'Экстренно\' ' \
            f' ELSE n.naz_extr_id::TEXT ' \
            f' END ' \
            f' FROM mm.mdoc AS m' \
            f' JOIN mm.hospdoc h ON h.mdoc_id = m.id' \
            f' JOIN mm.naz n ON n.mdoc_id = m.id' \
            f' JOIN mm.naz_type nt ON nt.id = n.naz_type_id' \
            f' JOIN mm.naz_type_dir ntd on ntd.id = nt.naz_type_dir_id' \
            f' JOIN mm.naz_action na ON na."id" = n.last_action_id' \
            f' JOIN mm.emp AS em ON  em.id = n.creator_emp_id' \
            f' JOIN mm.dept AS dp ON  dp.id = em.dept_id' \
            f' JOIN mm.people AS p ON  p.id = em.people_id' \
            f' JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id' \
            f' JOIN mm.naz_state ns ON ns.id = n.naz_state_id ' \
            f' WHERE n.create_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\' ' \
            f' AND n.actual_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\' ' \
            f' AND n.plan_dt BETWEEN \'{self.from_dt}\' AND \'{self.to_dt}\' ' \
            f' and n.create_dt between h.hosp_dt and coalesce(h.leave_dt,\'infinity\')' \
            f' and not ntd.path <@ (select array_agg(path) from mm.naz_type_dir where tags && array[\'GROUP_PAT\'::varchar])' \
            f' AND n.naz_view = \'{self.types_converting[self.research]}\'' \
            f' and na.state_value not in (\'cancelled\', \'postponed\' , \'completed\')' \
            f' AND dp.name =\'{self.dept}\''
 

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
                                                  port=actual_db['port'],
                                                  user=actual_db['user'],
                                                  password=actual_db['password'],
                                                  )
                    try:
                        cursor = connection.cursor()
                        cursor.execute(self.query_text)
                        selecting_data = cursor.fetchall()
                        return selecting_data
                    except (Exception, Error) as e:
                        return f'Ошибка в SQL запросе!\n\n{e}\n'
                    finally:
                        cursor.close()
                        connection.close()
                except (Exception, Error) as e:
                    return f'Ошибка подключения к БД!\n\n{e}\n'
            elif len(actual_db) > 1:
                return 'Проверьте настройки записей подключения к базе данных KIS.\n' \
                       ' Не должно быть более одной записи в статусе "active".'
            else:
                return 'Записи о подключении к базе данных KIS в статусе "inactive" \n'
        else:
            return 'Чтобы начать работу необходимо внести данные подключения к базе данных KIS через админ-панель.'


class ReadyReport:
    """ Represent HTML page and contains selected required data.
    The data converts to HTML code by Pandas DataFrame. Data for connecting get from app DB models. """
    def __init__(self, db_data):
        self.db_data = db_data
        if type(self.db_data) is str:
            self.dataframe = f'\t<p class="center-top-text">{self.db_data}</p>\n'
        elif type(self.db_data) is list and len(self.db_data) == 0:
            self.dataframe = string_snippets.tab_done
        else:
            row_values = len(self.db_data[0])
            rows_number = len(self.db_data)
            # List of lists of data separated and grouped inside
            data_lists = [list(map(lambda x: x[i], self.db_data)) for i in range(row_values)]
            # DataFrame's headers names for all type of researches
            headers_names = ['Врач', 'Номер ИБ', 'Пациент', 'Назначение',
                             'Дата создания', 'Назначено на дату', 'Статус']
            # 5 values in 1 row - if user chosen "Невыгруженные эпикризы"
            if row_values == 5:
                headers_names = ['ФИО пациента', 'ИБ пациента', 'Лечащий врач',
                                 'Дата подписи выписного эпикриза', 'Дата выписки пациента']
            # 6 values in 1 row - if user chosen "Невыгруженные эпикризы по всем отделениям"
            elif row_values == 6:
                headers_names = ['ФИО пациента', 'ИБ пациента', 'Заведующий отделением', 'Отделение',
                                 'Дата подписи выписного эпикриза', 'Дата выписки пациента']
            # Creating dict for DataFrame
            data = dict(zip(headers_names, data_lists))
            df = pd.DataFrame(data=data)
            first_column = df.columns[0]
            if first_column == 'ФИО пациента' and (len(df.columns) == 5 or len(df.columns) == 6):
                # Adding new column contains the different between today and sign date in DF
                df.insert(loc=len(df.columns), column='Не выгружено',
                          value=(today - df['Дата выписки пациента'].array).days)
                df.loc[df['Не выгружено'] < 0, 'Не выгружено'] = 0
                df.sort_values(by=['Не выгружено'], ascending=False, inplace=True)
            df.columns.rename('ID', inplace=True)
            df.index = range(1, rows_number + 1)
            self.dataframe = df

    def to_excel(self, dept):
        if type(self.dataframe) is not str:
            try:
                pathlib.Path('./WebApp/static/reports/').mkdir()
            except (FileExistsError, FileNotFoundError) as error:
                pass   
            first_column_name = self.dataframe.columns[0]
            if first_column_name == 'ID':
                ReportExcelWriter.xlsx_styles_epicrisis(dept_name=dept, frame=self.dataframe)
            else:
                ReportExcelWriter.xlsx_styles_researches(dept_name=dept, frame=self.dataframe)
        return

    def to_html(self, error_value=False):
        """ Prepare raw data getting from KIS DB and creating HTML template based on them. Data handled by PANDAS. """
        if error_value:
            # Date validations error text instead data table
            report = string_snippets.date_validation_error
        elif type(self.dataframe) is str:
            report = self.dataframe
        else:
            first_column_name = self.dataframe.columns[0]
            cnt = len(self.dataframe)
            if first_column_name == 'ФИО пациента':
                # Applying format to cells by condition
                report = self.dataframe.to_html(formatters=
                                        {
                                            # Formatting dates to string
                                            'Дата подписи выписного эпикриза': dates,
                                            'Дата выписки пациента': dates,
                                            # Formatting row by condition in a newer column "Не выгружено"
                                            'Не выгружено': overstay,
                                        },
                                        justify='center')
                report = report.replace('<th>ID</th>', '<th class="index-name">ID')
                report = report.replace('<td>Center', '<td style="text-align: center;">')
                # Changing color and style in the all ID's cells
                # Applying entire row color style where is text "over" (it is condition for dates comparison)
                report = re.sub(r'<tr>(.*?)</tr>', lambda match: style_and_remove_overcenter(match.group(1)),
                                report, flags=re.DOTALL)
                if self.dataframe.columns[0] == 'ФИО пациента' and len(self.dataframe.columns) == 7:
                    return report 
                report = string_snippets.download_button + f'\t\t<p class="center-top-cnt">Невыгруженные эпикризы:' \
                                                           f' {cnt}</p>\n\t\t<div class="table-container">\n' + report
            else:
                report = self.dataframe.to_html(justify="center", formatters={'Дата создания': dates,
                                                                              'Назначено на дату': dates})
                # Adding own class for further applying css for column "ID"
                report = re.sub(r'<tr style="text-align: center;">\s*<th>ID',
                                '<tr style="text-align: center;">\n\t  <th class="index-name">ID', report)
                # Result of creating dataframe and formatting to HTML
                report = string_snippets.download_button + \
                         f'\t\t<p class="center-top-cnt">Количество невыполненных назначений:' \
                         f' {cnt}</p>\n\t\t<div class="table-container">\n' + report
        return report
