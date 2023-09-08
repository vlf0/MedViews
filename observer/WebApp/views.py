# from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
# My own modules
from .forms import DeptChoose, ResearchType
from kisdb_connecting.operations import ReadyReportHTML, SelectAnswer, Queries
# from kisdb_connecting.operations import connecting, preparing_data, select_query


# Starting page (main) with the choice fields
def dept(request):
    # Fields to be sending to page (from our forms)
    depts_list = DeptChoose()
    return render(request=request, template_name='dept_name.html', context={'depts_list': depts_list})


def ref_to_type(request):
    chosen_dept = request.POST.get('dept_name')
    return redirect(to=research_type, chosen_dept=chosen_dept)


def research_type(request, chosen_dept):
    types_list = ResearchType()

    # Get the first part of URL path - department and reuse it
    # dept_from_url = request.path.split(sep='/')[1]

    return render(request=request, template_name='research_type.html', context={'types_list': types_list,
                                                                                'chosen_dept': chosen_dept})


def ref_to_output(request, chosen_dept):
    chosen_type = request.POST.get('research_types')
    return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type)


def output(request, chosen_dept, chosen_type):
    if request.method == 'POST':
        chosen_type = request.POST.get('research_types')
        # Handling data from db to HTML page by PANDAS
        query_text = Queries(dept=chosen_dept, research=chosen_type).ready_select()
        answer = SelectAnswer(query_text).selecting()
        ReadyReportHTML(answer).output_data()
        return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type)
    types_list = ResearchType()
    # Handling data from db to HTML page by PANDAS
    # Defined query class and call its method
    query_text = Queries(dept=chosen_dept, research=chosen_type).ready_select()
    # Defined answer class and call its method - this will ready data list from DB
    answer = SelectAnswer(query_text).selecting()
    # Preparing and outputting report on the page by pandas
    ReadyReportHTML(answer).output_data()
    return render(request=request, template_name='output.html', context={'types_list': types_list,
                                                                         'chosen_dept': chosen_dept})

