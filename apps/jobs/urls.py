from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('empresa/', views.company_job_list, name='company_job_list'),
    path('create/', views.create_offer, name='create_offer'),
    path('apply/', views.apply_offer, name='apply_offer'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
]
