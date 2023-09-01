from django.shortcuts import render, redirect
from django.contrib import messages
# My own modules
from .forms import DeptChoose, ResearchType
from kisdb_connecting.operations import connecting, preparing_data


# Starting page (main)
def index(request):
    # Fields to be sending to page (from our forms)
    depts_list = DeptChoose()
    research_list = ResearchType()
    return render(request=request, template_name='index.html', context={'depts_list': depts_list,
                                                                        'research_list': research_list})


def reporting(request):
    dept = request.POST.get('dept_name')
    if dept in ['Педиатрия', 'Хирургия']:
        return redirect(to='output')
    messages.error(request, 'Error')
    return redirect(to='index')
    # return render(request=request, template_name='output.html')


def output(request):
    preparing_data(connecting())
    return render(request=request, template_name='output.html')

# Redirecting to reporting page
# def reporting(request):
#     dept = request.POST.get('dept_name')
#     print(dept)
#     for depts in ['Педиатрия', 'Хирургия', 'Кардио']:
#         if depts == dept:
#             return redirect(to='reporting')
#     messages.error(request, 'Error')
#     return redirect(to='index')
