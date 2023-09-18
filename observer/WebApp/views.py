import http.client

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json
# My own modules
from .forms import DeptChoose, ResearchType, DateButtons
from kisdb_connecting.operations import ReadyReportHTML, SelectAnswer, Queries
from .local_functions import FrontDataValues, months, date_converter, date_pg_format, calendar_create


# Decorator that let us avoid django CSRF protection method.
@csrf_exempt
def api_func(request):
    """ Getting data values gotten from frontend by JS
    and create class's obj based for them.
     Workpiece for future.
    """
    data = json.loads(request.body)
    FrontDataValues(value=data).adding()
    return JsonResponse({'message': 'GOT DATA'}, status=200)


def dept(request):
    depts_list = DeptChoose()
    if type(depts_list.depts) is str:
        return render(request=request, template_name='errors.html',
                      context={'error_text': depts_list.depts})
    # Fields to be sending to page (from our forms)
    context = {'depts_list': depts_list}
    return render(request=request, template_name='dept_name.html', context=context)


def ref_to_type(request):
    chosen_dept = request.POST.get('dept_name')
    return redirect(to=research_type, chosen_dept=chosen_dept)


def research_type(request, chosen_dept):
    types_list = ResearchType()
    # if type(types_list.r_types) is str:
    #     return render(request=request, template_name='errors.html',
    #                   context={'error_text': types_list.r_types})
    date_buttons = DateButtons()
    doc = SelectAnswer(query_text=f'SELECT doc_fio FROM mm.dbkis WHERE dept = \'{chosen_dept}\'').selecting()
    # Checking if doctor belong this dept
    if len(doc) == 0:
        doc = 'заведующий не может быть назначен неработающему отделению.'
    else:
        doc = doc[0][0]
    context = {'types_list': types_list, 'chosen_dept': chosen_dept, 'doc': doc,
               'date_buttons': date_buttons, 'calendar': calendar_create()}
    return render(request=request, template_name='research_type.html', context=context)


def ref_to_output(request, chosen_dept):
    prep_dates = date_pg_format(request.POST.get)
    # Dates to send on page into information line
    try:
        from_dt = '-'.join(prep_dates[:3])
        to_dt = '-'.join(prep_dates[3:])
    except TypeError as er:
        print(f'\n{er}\n')
        pass
    # Get research type from FORM fields
    chosen_type = request.POST.get('research_types')
    return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type,
                    from_dt=from_dt, to_dt=to_dt)


def output(request, chosen_dept, chosen_type, from_dt, to_dt):
    # Sql query to DB
    query_text = Queries(dept=chosen_dept, research=chosen_type, from_dt=from_dt, to_dt=to_dt).ready_select()
    # Connecting to DB and execute query
    answer = SelectAnswer(query_text).selecting()
    # Creating full reporting page contains prepared data got from DB by PANDAS
    ReadyReportHTML(answer).output_data()
    # Forms on page
    # Dict containing date values user inserted
    choice = {'research_types': chosen_type}
    dates = {'from_dt': from_dt, 'to_dt': to_dt}
    # Parameter data is actual values that will initial
    types_list = ResearchType(data=choice)
    date_buttons = DateButtons(data=dates)
    if request.method == 'POST':
        prep_dates = date_pg_format(request.POST.get)
        chosen_type = request.POST.get('research_types')
        # Dates to send on page into information line
        from_dt = '-'.join(prep_dates[:3])
        to_dt = '-'.join(prep_dates[3:])
        return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type, from_dt=from_dt, to_dt=to_dt)
    doc = SelectAnswer(query_text=f'SELECT doc_fio FROM mm.dbkis WHERE dept = \'{chosen_dept}\'').selecting()
    # Checking if doctor belong this dept
    if len(doc) == 0:
        doc = 'заведующий не может быть назначен неработающему отделению.'
    else:
        doc = doc[0][0]
    context = {'types_list': types_list, 'chosen_dept': chosen_dept,
               'doc': doc, 'date_buttons': date_buttons, 'from_dt': date_converter(from_dt),
               'to_dt': date_converter(to_dt), 'chosen_type': chosen_type}
    return render(request=request, template_name='output.html', context=context)

