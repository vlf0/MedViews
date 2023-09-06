from django import forms
from django.db import models


class DeptChoose(forms.Form):
    """ Represent drop-down list of departments
        name from KIS DB on the starting page. """

    # List of the all depts from KIS DB
    # depts = KIS_Model.objects.all()
    # depts_tuple = []
    #
    # # Iterations and converting depts string in tuple
    # # Because in requesting only tuple(tuple(str, str), tuple(str, str), ...)
    # for field in depts:
    #     depts_tuple.append(tuple([field, field]))

    # Choice field on the page with ready drop-down list
    dept_name = forms.ChoiceField(label='Отделение', choices=(('dept_1', 'dept_1'), ('dept_2', 'dept_2')))


class ResearchType(forms.Form):
    """ Represent drop-down list of research
        name from KIS DB on the starting page. """

    research_types = forms.ChoiceField(label='Тип незакрытых назначений',
                                       choices=(('Назначено', 'Назначено'),
                                                ('Отменено', 'Отменено')))
