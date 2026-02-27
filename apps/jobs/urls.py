from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.create_offer, name='create_offer'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
]
