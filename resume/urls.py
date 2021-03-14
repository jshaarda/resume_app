from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.JobView.as_view(), name='job_list'),
    path('jobs/<int:pk>', views.JobDetailView.as_view(), name='job_detail'),
    path('skills/', views.SkillView.as_view(), name='skill_list'),
    path('projects/', views.ProjectView.as_view(), name='project_list'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('print/', views.print_view, name='print_view'),
]
