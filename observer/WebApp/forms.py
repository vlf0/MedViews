from django import forms
from django.db import models


class DeptChoose(forms.Form):
    """ This class represent dept choosing form on the page. """

    # List of the all depts from KIS DB
    # depts = KIS_Model.objects.all()
    # depts_tuple = []
    #
    # # Iterations and converting depts string in tuple
    # # Because in requesting only tuple(tuple(str, str), tuple(str, str), ...)
    # for field in depts:
    #     depts_tuple.append(tuple([field, field]))

    # Choice field on the page with ready drop-down list
    dept_name = forms.ChoiceField(label='Отделение', choices=(('ПАО', 'ПАО'), ('Педиатрия', 'Педиатрия'),
                                                              ('Хиругия', 'Хиругия'), ('Кардио', 'Кардио')))


