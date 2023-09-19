from datetime import date, timedelta
from django import forms

# Import my own modules
from kisdb_connecting.operations import SelectAnswer, Queries
from kisdb_connecting.string_snippets import depts_list


def converting(x):
    result = []
    for i in x:
        result.append((i, i))
    return tuple(result)


class DeptChoose(forms.Form):
    """ Represent drop-down list of departments name from KIS DB on the starting page. """
    # Create object that contains all departments from KIS DB and create list generator
    depts = SelectAnswer(query_text=depts_list).selecting()
    # Call exception and redirect to page with its text
    if type(depts) is str:
        pass
    # Creating form and redirect to depts choice page
    elif type(depts) is list:
        str_values = [field[0] for field in depts]
        # Choice field on the page with ready drop-down list
        dept_name = forms.ChoiceField(label='Отделение', choices=converting(str_values),
                                      widget=forms.Select(attrs={'class': 'dept-custom'})
                                      )


class ResearchType(forms.Form):
    """ Represent drop-down list of research name from KIS DB on the starting page. """
    research_types = forms.ChoiceField(label='Тип исследования',
                                       choices=(('Лабораторные исследования', 'Лабораторные исследования'),
                                                ('Инструментальные исследования', 'Инструментальные исследования'),
                                                ('Процедуры и манипуляции', 'Процедуры и манипуляции'),
                                                ('Операции', 'Операции'),
                                                ('Консультации', 'Консультации')
                                                ),
                                       widget=forms.Select(attrs={'class': 'r_type-custom'})
                                       )


class DateButtons(forms.Form):
    """ Represent buttons of date type on the page. It is the 3rd sql condition in query. """
    from_dt = forms.DateField(label='Начало периода',
                              widget=forms.DateInput(attrs={'type': 'date', 'class': 'datefield-custom'}),
                              )
    to_dt = forms.DateField(label='Конец периода', required=True,
                            widget=forms.DateInput(attrs={'type': 'date', 'class': 'datefield-custom'}),
                            )

