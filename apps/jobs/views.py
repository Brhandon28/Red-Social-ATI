from django.shortcuts import render


def job_list(request):
    return render(request, 'jobs/job_list.html')


def job_detail(request, job_id):
    return render(request, 'jobs/job_detail.html', {'job_id': job_id})
