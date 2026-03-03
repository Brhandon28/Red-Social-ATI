from django.contrib import messages
from django.shortcuts import redirect, render


SAMPLE_JOBS = [
    {
        'id': 1,
        'company': 'Nombre de Empresa',
        'title': 'Título de empleo',
        'location': 'Ubicación',
        'age': '20 h',
        'summary': 'morbi at sem facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus ipsum nec nibh lacus, suspendisse',
    },
    {
        'id': 2,
        'company': 'Faucibus molestie',
        'title': 'Nombre de empleo',
        'location': 'Tellus neque',
        'age': '2 d',
        'summary': 'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac sapien enim nulla tellus risus ornare lobortis commodo in proin.',
    },
    {
        'id': 3,
        'company': 'Faucibus molestie',
        'title': 'Nombre de empleo',
        'location': 'Tellus neque',
        'age': '2 d',
        'summary': 'Commodo in proin in fermentum morbi at sem facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus ipsum nec nibh lacus.',
    },
    {
        'id': 4,
        'company': 'Faucibus molestie',
        'title': 'Nombre de empleo',
        'location': 'Tellus neque',
        'age': '2 d',
        'summary': 'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac sapien enim nulla tellus risus ornare.',
    },
    {
        'id': 5,
        'company': 'Faucibus molestie',
        'title': 'Nombre de empleo',
        'location': 'Tellus neque',
        'age': '2 d',
        'summary': 'Morbi at sem facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus ipsum nec nibh lacus, suspendisse.',
    },
]


def _get_session_jobs(request):
    return request.session.get('jobs_created', [])


def _save_session_jobs(request, jobs):
    request.session['jobs_created'] = jobs


def _build_jobs_for_ui(request):
    session_jobs = _get_session_jobs(request)
    return session_jobs + SAMPLE_JOBS


def _next_job_id(jobs):
    if not jobs:
        return 1
    return max(job['id'] for job in jobs) + 1


def _get_current_user_profile(request):
    current_username = (getattr(request, 'hardcoded_user', '') or '').strip()
    if current_username:
        return {
            'display_name': current_username.capitalize(),
            'role': 'Cuenta personal',
        }
    return {
        'display_name': 'Usuario',
        'role': 'Cuenta personal',
    }


def job_list(request):
    user_profile = _get_current_user_profile(request)
    jobs = _build_jobs_for_ui(request)
    recommendations = jobs[:2]
    suggested_jobs = jobs[2:5]
    recent_searches = [
        {
            'title': 'List item',
            'description': 'Supporting line text lorem ipsum dolor sit amet, consectetur.',
        },
        {
            'title': 'List item',
            'description': 'Supporting line text lorem ipsum dolor sit amet, consectetur.',
        },
    ]

    return render(
        request,
        'jobs/job_list.html',
        {
            'jobs': jobs,
            'recommendations': recommendations,
            'suggested_jobs': suggested_jobs,
            'recent_searches': recent_searches,
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )


def company_job_list(request):
    user_profile = _get_current_user_profile(request)
    jobs = _build_jobs_for_ui(request)
    own_offers = jobs[:2]
    suggested_jobs = jobs[2:5]

    return render(
        request,
        'jobs/company_job_list.html',
        {
            'own_offers': own_offers,
            'suggested_jobs': suggested_jobs,
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )


def job_detail(request, job_id):
    jobs = _build_jobs_for_ui(request)
    selected_job = next((job for job in jobs if job['id'] == job_id), jobs[0])
    similar_jobs = [job for job in jobs if job['id'] != selected_job['id']]

    return render(
        request,
        'jobs/apply_job_offer.html',
        {
            'job': selected_job,
            'similar_jobs': similar_jobs,
        },
    )


def apply_offer(request):
    jobs = _build_jobs_for_ui(request)
    selected_job = jobs[0]
    similar_jobs = [job for job in jobs if job['id'] != selected_job['id']]

    return render(
        request,
        'jobs/apply_job_offer.html',
        {
            'job': selected_job,
            'similar_jobs': similar_jobs,
        },
    )


def create_offer(request):
    form_data = {
        'name': '',
        'title': '',
        'description': '',
        'location': '',
        'salary_range': '',
    }

    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'title': request.POST.get('title', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'location': request.POST.get('location', '').strip(),
            'salary_range': request.POST.get('salary_range', '').strip(),
        }

        if not form_data['name'] or not form_data['title'] or not form_data['description'] or not form_data['location']:
            messages.error(request, 'Completa todos los campos obligatorios para crear la oferta.')
            return render(request, 'jobs/create_job_offer.html', {'form_data': form_data})

        jobs_for_ui = _build_jobs_for_ui(request)
        new_job = {
            'id': _next_job_id(jobs_for_ui),
            'company': form_data['name'],
            'title': form_data['title'],
            'location': form_data['location'],
            'age': 'Ahora',
            'summary': form_data['description'],
            'salary_range': form_data['salary_range'],
        }

        session_jobs = _get_session_jobs(request)
        session_jobs.insert(0, new_job)
        _save_session_jobs(request, session_jobs)

        messages.success(request, 'La oferta de empleo se creó correctamente.')
        return redirect('jobs:job_detail', job_id=new_job['id'])

    return render(request, 'jobs/create_job_offer.html', {'form_data': form_data})
