import datetime
from django import forms
from django.db import models

# Import my own modules
from kisdb_connecting.operations import SelectAnswer, Queries


class DeptChoose(forms.Form):
    """ Represent drop-down list of departments name from KIS DB on the starting page. """
    # Create object that contains all departments from KIS DB and create list generator
    answer = SelectAnswer(query_text='SELECT name FROM mm.depts d').selecting()
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
    from_dt = forms.DateField(required=True, initial=(datetime.date.today()-datetime.timedelta(days=14)))
    to_dt = forms.DateField(required=True, initial=datetime.date.today())

