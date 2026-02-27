from django.shortcuts import render


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


def job_list(request):
    return render(request, 'jobs/job_list.html', {'jobs': SAMPLE_JOBS})


def job_detail(request, job_id):
    selected_job = next((job for job in SAMPLE_JOBS if job['id'] == job_id), SAMPLE_JOBS[0])
    similar_jobs = [job for job in SAMPLE_JOBS if job['id'] != selected_job['id']]

    return render(
        request,
        'jobs/create_job_offer.html',
        {
            'job': selected_job,
            'similar_jobs': similar_jobs,
        },
    )


def create_offer(request):
    selected_job = SAMPLE_JOBS[0]
    similar_jobs = [job for job in SAMPLE_JOBS if job['id'] != selected_job['id']]

    return render(
        request,
        'jobs/create_job_offer.html',
        {
            'job': selected_job,
            'similar_jobs': similar_jobs,
        },
    )
