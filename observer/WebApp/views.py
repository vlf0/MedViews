# from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# My own modules
from .forms import DeptChoose, ResearchType
from kisdb_connecting.operations import connecting, preparing_data, select_query


# Starting page (main) with the choice fields
def dept(request):
    # Fields to be sending to page (from our forms)
    depts_list = DeptChoose()
    return render(request=request, template_name='index.html', context={'depts_list': depts_list})


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


# Just displaying template with django URL parameter by getting previous POST data
def output(request, chosen_dept, chosen_type):
    if request.method == 'POST':
        chosen_type = request.POST.get('research_types')
        preparing_data(connecting(select_query(chosen_dept, chosen_type)))
        return redirect(to=output, chosen_dept=chosen_dept, chosen_type=chosen_type)
    else:
        preparing_data(connecting(select_query(chosen_dept, chosen_type)))
        types_list = ResearchType()
        return render(request=request, template_name='output.html', context={'types_list': types_list,
                                                                             'chosen_dept': chosen_dept})


# def ref_second_output(request, ):
#     return redirect()

