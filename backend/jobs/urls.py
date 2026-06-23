from django.urls import path
from .views import job_list, job_detail, apply_job, save_job

app_name = 'jobs'

urlpatterns = [
    path('', job_list, name='job_list'),
    path('<int:job_id>/', job_detail, name='job_detail'),
    path('<int:job_id>/apply/', apply_job, name='apply_job'),
    path('<int:job_id>/save/', save_job, name='save_job'),
]