from django.shortcuts import render, redirect
from django.contrib import messages
# My own modules
from .forms import DeptChoose, ResearchType
from kisdb_connecting.operations import connecting, preparing_data, select_query

naz_type = ''


# Starting page (main)
def index(request):
    # Fields to be sending to page (from our forms)
    depts_list = DeptChoose()
    research_list = ResearchType()
    return render(request=request, template_name='index.html', context={'depts_list': depts_list,
                                                                        'research_list': research_list})


def reporting(request):
    global naz_type
    dept = request.POST.get('dept_name')
    naz_type = request.POST.get('research_types')
    if dept in ['Педиатрия', 'Хирургия']:
        # Redirecting to reporting page
        return redirect(to='output')
    messages.error(request, 'Error')
    return redirect(to='index')
    # return render(request=request, template_name='output.html')


def output(request):
    query = select_query(naz_type)
    preparing_data(connecting(query))
    return render(request=request, template_name='output.html')

