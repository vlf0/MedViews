from django.urls import path
from . import views


urlpatterns = [
    path('', views.dept, name='dept'),
    path('test/', views.test, name='test'),
    path('ref_to_type/', views.ref_to_type, name='ref_to_type'),
    path('<str:chosen_dept>/research_type/', views.research_type, name='research_type'),
    path('downloading/<str:chosen_dept>/', views.downloading, name='downloading'),
    # Redirect to changed page with errors displaying
    path('<str:chosen_dept>/<str:research_type>/', views.research_type, name='research_type'),
    path('<str:chosen_dept>/ref_to_output', views.ref_to_output, name='ref_to_output'),
    path('<str:chosen_dept>/<str:chosen_type>/<str:from_dt>:<str:to_dt>/', views.output, name='output'),
    # Redirect to changed page with errors displaying
    path('<str:chosen_dept>/<str:chosen_type>/<str:from_dt>:<str:to_dt>/<str:error>/', views.output, name='output')
]
