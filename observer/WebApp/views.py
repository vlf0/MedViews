from datetime import date, timedelta
from django.shortcuts import render, redirect
# My own modules
from .forms import DeptChoose, ResearchType, DateButtons
from kisdb_connecting.operations import ReadyReport, SelectAnswer, Queries
from .local_functions import months, date_converter, validate_dates
from kisdb_connecting.string_snippets import date_validation_error


def test(request):
    return render(request=request, template_name='test.html')


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


def research_type(request, chosen_dept, research_type=None):
    # Converted to string format for insert to fields on browser in the first refer
    from_dt_initial = (date.today() - timedelta(days=14)).strftime('%Y-%m-%d')
    to_dt_initial = date.today().strftime('%Y-%m-%d')
    # Form fields definite
    date_buttons = DateButtons(initial={'from_dt': from_dt_initial, 'to_dt': to_dt_initial})
    types_list = ResearchType()
    doc = SelectAnswer(query_text=f'SELECT doc_fio FROM mm.dbkis WHERE dept = \'{chosen_dept}\'').selecting()
    # Checking if doctor belong this dept
    if len(doc) == 0:
        doc = 'заведующий не может быть назначен неработающему отделению.'
    else:
        doc = doc[0][0]
    context = {'types_list': types_list, 'chosen_dept': chosen_dept, 'doc': doc,
               'date_buttons': date_buttons}

    if research_type:
        types_list = ResearchType(initial={'research_types': research_type})
        context = {'types_list': types_list, 'chosen_dept': chosen_dept, 'doc': doc,
                   'date_buttons': date_buttons, 'error': date_validation_error}

    return render(request=request, template_name='research_type.html', context=context)


def ref_to_output(request, chosen_dept):
    # Dates to send on page into information line
    from_dt = request.POST.get('from_dt')
    to_dt = request.POST.get('to_dt')
    # Get research type from FORM fields
    chosen_type = request.POST.get('research_types')
    if not validate_dates(first_date=from_dt, second_date=to_dt):
        return redirect(to=research_type, chosen_dept=chosen_dept, research_type=chosen_type)

    return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type,
                    from_dt=from_dt, to_dt=to_dt)


def output(request, chosen_dept, chosen_type, from_dt, to_dt, error=None):
    # Preparing dates in format matches with hosp personal
    from_dt_dbformat = from_dt + ' 00:00:00'
    to_db_dbformat = to_dt + ' 23:59:59'
    # Sql query to DB
    query_text = Queries(dept=chosen_dept, research=chosen_type,
                         from_dt=from_dt_dbformat, to_dt=to_db_dbformat).ready_select()
    # Connecting to DB and execute query
    answer = SelectAnswer(query_text).selecting()
    common_rows_number = len(answer)
    # Creating full reporting page contains prepared data got from DB by PANDAS
    ReadyReport(answer).to_excel(dept=chosen_dept)
    ReadyReport(answer).to_html()
    if error:
        ReadyReport(answer).to_html(error_value=True)
    # Forms on page
    # Dict containing date values user inserted
    choice = {'research_types': chosen_type}
    dates = {'from_dt': from_dt, 'to_dt': to_dt}
    # Parameter data is actual values that will initial
    types_list = ResearchType(data=choice)
    date_buttons = DateButtons(data=dates)

    if request.method == 'POST':
        chosen_type = request.POST.get('research_types')
        # Dates to send on page into information line
        from_dt = request.POST.get('from_dt')
        to_dt = request.POST.get('to_dt')
        # Dates validating
        if not validate_dates(first_date=from_dt, second_date=to_dt):
            from_dt = (date.today() - timedelta(days=14)).strftime('%Y-%m-%d')
            to_dt = date.today().strftime('%Y-%m-%d')
            return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type,
                            from_dt=from_dt, to_dt=to_dt, error='error')
        return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type, from_dt=from_dt, to_dt=to_dt)

    doc = SelectAnswer(query_text=f'SELECT doc_fio FROM mm.dbkis WHERE dept = \'{chosen_dept}\'').selecting()
    # Checking if doctor belong this dept
    if len(doc) == 0:
        doc = 'заведующий не может быть назначен неработающему отделению.'
    else:
        doc = doc[0][0]
    context = {'types_list': types_list, 'chosen_dept': chosen_dept,
               'doc': doc, 'date_buttons': date_buttons, 'from_dt': date_converter(from_dt),
               'to_dt': date_converter(to_dt), 'chosen_type': chosen_type, 'common_rows_number': common_rows_number}
    return render(request=request, template_name='output.html', context=context)

