# from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
# My own modules
from .forms import DeptChoose, ResearchType, DateButtons
from kisdb_connecting.operations import ReadyReportHTML, SelectAnswer, Queries
# from kisdb_connecting.operations import connecting, preparing_data, select_query


def dept(request):
    depts_list = DeptChoose()
    if type(depts_list.depts) is str:
        error_text = 'Ошибка выборки отделений.'
        return render(request=request, template_name='errors.html',
                      context={'error_text': error_text})
    # Fields to be sending to page (from our forms)
    context = {'depts_list': depts_list}
    return render(request=request, template_name='dept_name.html', context=context)


def ref_to_type(request):
    chosen_dept = request.POST.get('dept_name')
    return redirect(to=research_type, chosen_dept=chosen_dept)


def research_type(request, chosen_dept):
    types_list = ResearchType()
    print(types_list)
    # if type(types_list.r_types) is str:
    #     error_text = 'Ошибка выборки типов исследований.'
    #     return render(request=request, template_name='errors.html',
    #                   context={'error_text': error_text})
    date_buttons = DateButtons()
    doc = SelectAnswer(query_text=f'SELECT mm.emp_get_fio_by_id(dp.manager_emp_id) as Заведующий_отделением FROM mm.dept dp WHERE dp.name = \'{chosen_dept}\'').selecting()[0][0]
    context = {'types_list': types_list, 'chosen_dept': chosen_dept, 'doc': doc, 'date_buttons': date_buttons}
    return render(request=request, template_name='research_type.html', context=context)


def ref_to_output(request, chosen_dept):
    # Get research type from FORM fields
    chosen_type = request.POST.get('research_types')
    # Get FROM data from FORM fields by creating list generator of date values
    from_dt = [request.POST.get(i) for i in request.POST if i in ['from_dt_month',
                                                                  'from_dt_day',
                                                                  'from_dt_year']
               ]
    # Converting date format to Postgres format (yyyy-mm-dd)
    # because another way - change postgresql.conf file KIS DB
    from_dt.insert(0, from_dt.pop())
    from_dt = '-'.join(from_dt)
    # Get TO data from FORM fields by creating list generator of date values
    to_dt = [request.POST.get(i) for i in request.POST if i in ['to_dt_month', 'to_dt_day', 'to_dt_year']]
    to_dt.insert(0, to_dt.pop())
    to_dt = '-'.join(to_dt)
    return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type,
                    from_dt=from_dt, to_dt=to_dt)


def output(request, chosen_dept, chosen_type, from_dt, to_dt):
    if request.method == 'POST':
        chosen_type = request.POST.get('research_types')
        # Get FROM data from FORM fields by creating list generator of date values
        from_dt = [request.POST.get(i) for i in request.POST if i in ['from_dt_month',
                                                                      'from_dt_day',
                                                                      'from_dt_year']
                   ]
        # Converting date format to Postgres format (yyyy-mm-dd)
        # because another way - change postgresql.conf file KIS DB
        from_dt.insert(0, from_dt.pop())
        from_dt = '-'.join(from_dt)
        # Get TO data from FORM fields by creating list generator of date values
        to_dt = [request.POST.get(i) for i in request.POST if i in ['to_dt_month', 'to_dt_day', 'to_dt_year']]
        to_dt.insert(0, to_dt.pop())
        to_dt = '-'.join(to_dt)
        # Handling data from db to HTML page by PANDAS
        query_text = Queries(dept=chosen_dept, research=chosen_type, from_dt=from_dt, to_dt=to_dt).ready_select()
        answer = SelectAnswer(query_text).selecting()
        ReadyReportHTML(answer).output_data()
        return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type, from_dt=from_dt, to_dt=to_dt)
    types_list = ResearchType()
    date_buttons = DateButtons()
    # Handling data from db to HTML page by PANDAS
    # Defined query class and call its method
    query_text = Queries(dept=chosen_dept, research=chosen_type, from_dt=from_dt, to_dt=to_dt).ready_select()
    # Defined answer class and call its method - this will ready data list from DB
    answer = SelectAnswer(query_text).selecting()
    # Preparing and outputting report on the page by pandas
    ReadyReportHTML(answer).output_data()
    doc = SelectAnswer(query_text=f'SELECT mm.emp_get_fio_by_id(dp.manager_emp_id) as Заведующий_отделением FROM mm.dept dp WHERE dp.name = \'{chosen_dept}\'').selecting()[0][0]
    context = {'types_list': types_list, 'chosen_dept': chosen_dept, 'doc': doc, 'date_buttons': date_buttons}
    return render(request=request, template_name='output.html', context=context)

