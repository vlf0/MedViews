download_button = (
        '\t<div class="download_button-container">\n'
        '\t\t<button form="download_report" type="submit" class="download_button">\n'
        '\t\t<img src="/static/dwnld_logo.png"><p>Сохранить в Excel</p> </button>\n'
        '\t</div>\n'
        )


tab_done = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n\t<div>\n'

date_validation_error = '\t\t<p class="center-top-text">Дата окончания периода не может быть меньше даты начала!</p>\n'



depts_by_ids = 'SELECT d.name FROM mm.dept d'

common_simi_query = 'SELECT pat_fio, pat_ib, zav, dept, sign_dt, pat_leave_dt FROM mm.tap'

