from datetime import date, timedelta
from django import forms
from django.db import models

# Import my own modules
from kisdb_connecting.operations import SelectAnswer, Queries


class DeptChoose(forms.Form):
    """ Represent drop-down list of departments name from KIS DB on the starting page. """
    # Create object that contains all departments from KIS DB and create list generator
    answer = SelectAnswer(query_text='SELECT d.name FROM mm.dept d' \
            ' WHERE d.id IN (\'b99a5265-74c0-4ace-8cb3-1fe204b59aaf\', \'faf07796-1ffb-478e-a06e-717dfc46a7ec\',' \
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
            ' \'5fe0204b-e340-486a-94db-2bcc75fc6e64\', \'7168f375-ac21-4c66-9575-f033c3ac0cd3\')'
                          ).selecting()
    str_values = [field[0] for field in answer]

    @staticmethod
    def converting(x):
        """ Defined method that create tuple of sequence of tuples that send to form the choices list on the page. """
        result = []
        for i in x:
            result.append((i, i))
        return tuple(result)
    # Choice field on the page with ready drop-down list
    dept_name = forms.ChoiceField(label='Отделение', choices=converting(str_values))


class ResearchType(forms.Form):
    """ Represent drop-down list of research name from KIS DB on the starting page. """
    research_types = forms.CharField(required=True)


class DateButtons(forms.Form):
    """ Represent buttons of date type on the page. It is the 3rd sql condition in query. """
    from_dt = forms.DateField(widget=forms.SelectDateWidget(years=range(date.today().year, date.today().year-5, -1)),
                              initial=date.today()-timedelta(days=14))
    to_dt = forms.DateField(widget=forms.SelectDateWidget(years=range(date.today().year, date.today().year-5, -1)),
                            initial=date.today())

