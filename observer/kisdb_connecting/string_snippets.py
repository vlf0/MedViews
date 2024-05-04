download_button = (
        '\t<div class="download_button-container">\n'
        '\t\t<button form="download_report" type="submit" class="download_button">\n'
        '\t\t<img src="/static/excel_logo.png"><p>Сохранить в Excel</p> </button>\n'
        '\t</div>\n'
        )

tab_done = '\t<p class="center-top-text">По заданным параметрам все исследования выполнены.</p>\n'

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

common_simi_query = 'SELECT mm.famaly_io(m.surname,m.name,m.patron) AS ФИО_Пациента,' \
                    ' concat_ws (\' - \',m.num,m.YEAR) AS №ИБ,' \
                    ' mm.emp_get_fio_by_id (d.manager_emp_id ) AS Заведующий_отделением,' \
                    ' d.name AS Отделение,' \
                    ' tt.sign_dt AS Дата_подписи_леч_врачом,' \
                    ' h.leave_dt AS Дата_выписки_пациента' \
                    ' FROM mm.hospdoc h' \
                    ' JOIN mm.mdoc m ON m.id = h.mdoc_id' \
                    ' JOIN mm.people p ON p.id = m.people_id' \
                    ' JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id' \
                    ' LEFT JOIN mm.dept d ON d.id = h.dept_id' \
                    ' JOIN (SELECT et.ehr_case_id, et.sign_dt,' \
                    ' et.epic_code,' \
                    ' et.creator_emp_id AS emp_id' \
                    ' FROM mm.epic_text et' \
                    ' WHERE  et.epic_code IN  (\'Z00.001.008\', \'Z00.001.012\', \'Z00.004.032\', \'Z00.001.014\', \'Z00.001.009\', \'Z00.001.016\')' \
                    ' AND et.create_dt >= \'01.01.2023\'' \
                    ' and et.allow_export = 2' \
                    ' AND et.ehr_case_id NOT IN' \
                    ' (SELECT hoer.ehr_case_id' \
                    ' FROM mm.hospdoc_out_emiac_remd hoer' \
                    ' WHERE hoer.create_dt >= \'01.01.2023\'' \
                    ' AND hoer.status = 1)' \
                    ' AND et.sign_dt NOTNULL)tt ON tt.ehr_case_id = h.ehr_case_id' \
                    ' AND h.leave_dt NOTNULL' \
                    ' ORDER BY h.leave_dt ASC'

