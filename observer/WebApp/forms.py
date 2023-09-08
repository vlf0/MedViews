from django import forms
from django.db import models

from kisdb_connecting.operations import SelectAnswer, Queries


class DeptChoose(forms.Form):
    """ Represent drop-down list of departments
        name from KIS DB on the starting page. """
    # Create object that contains all departments from KIS DB
    answer = SelectAnswer(query_text='SELECT name FROM mm.depts d').selecting()
    str_values = [field[0] for field in answer]

    # Defined method that create tuple(tuple(str, str), tuple(str, str), ...)
    # It will be the choices list on the page
    @staticmethod
    def converting(x):
        result = []
        for i in x:
            result.append((i, i))
        return tuple(result)
    print(converting(str_values))

    # # For testing on the pages
    # dept_name = forms.CharField(required=True)

    # Choice field on the page with ready drop-down list
    dept_name = forms.ChoiceField(label='Отделение', choices=converting(str_values))



class ResearchType(forms.Form):
    """ Represent drop-down list of research
        name from KIS DB on the starting page. """

    # research_types = forms.ChoiceField(label='Тип незакрытых назначений',
    #                                    choices=(('Назначено', 'Назначено'),
    #                                             ('Отменено', 'Отменено')))
    research_types = forms.CharField(required=True)
