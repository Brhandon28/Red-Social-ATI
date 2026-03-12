from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import BooleanField, Count, Exists, OuterRef, Value
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import JobApplication, JobOffer


def _get_current_user_profile(request):
	user = request.user
	if user.is_authenticated:
		return {
			'display_name': str(user),
			'role': user.get_tipoUsuario_display() if hasattr(user, 'get_tipoUsuario_display') else 'Cuenta personal',
		}
	return {
		'display_name': 'Usuario',
		'role': 'Cuenta personal',
	}


def _is_company_user(user):
	return getattr(user, 'tipoUsuario', None) == 'empresa'


def _offers_queryset_for_user(user):
	offers = JobOffer.objects.select_related('created_by').annotate(
		applications_count=Count('applications', distinct=True),
	)

	if user.is_authenticated:
		return offers.annotate(
			applied_by_me=Exists(
				JobApplication.objects.filter(offer=OuterRef('pk'), applicant=user)
			)
		)

	return offers.annotate(applied_by_me=Value(False, output_field=BooleanField()))


@login_required
def job_list(request):
	user_profile = _get_current_user_profile(request)
	offers = _offers_queryset_for_user(request.user)

	recommendations = offers[:2]
	suggested_jobs = offers[2:5]
	recent_searches = [
		{
			'title': 'Ultimas ofertas publicadas',
			'description': 'Explora nuevas oportunidades creadas recientemente.',
		},
		{
			'title': 'Ofertas en tu zona',
			'description': 'Filtra por ubicacion para encontrar empleo cerca de ti.',
		},
	]

	return render(
		request,
		'jobs/job_list.html',
		{
			'jobs': offers,
			'recommendations': recommendations,
			'suggested_jobs': suggested_jobs,
			'recent_searches': recent_searches,
			'current_user_display_name': user_profile['display_name'],
			'current_user_role': user_profile['role'],
		},
	)


@login_required
def company_job_list(request):
	if not _is_company_user(request.user):
		messages.error(request, 'Esta seccion esta disponible solo para cuentas empresa.')
		return redirect('jobs:job_list')

	user_profile = _get_current_user_profile(request)
	offers = _offers_queryset_for_user(request.user)
	own_offers = offers.filter(created_by=request.user)
	suggested_jobs = offers.exclude(created_by=request.user)[:3]

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


@login_required
def job_detail(request, job_id):
	selected_job = get_object_or_404(_offers_queryset_for_user(request.user), pk=job_id)
	similar_jobs = _offers_queryset_for_user(request.user).exclude(pk=selected_job.pk)[:6]

	return render(
		request,
		'jobs/apply_job_offer.html',
		{
			'job': selected_job,
			'similar_jobs': similar_jobs,
		},
	)


@login_required
def create_offer(request):
	if not _is_company_user(request.user):
		messages.error(request, 'Solo una cuenta empresa puede crear ofertas de empleo.')
		return redirect('jobs:job_list')

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

		required_fields = ['name', 'title', 'description', 'location']
		if any(not form_data[field] for field in required_fields):
			messages.error(request, 'Completa todos los campos obligatorios para crear la oferta.')
			return render(request, 'jobs/create_job_offer.html', {'form_data': form_data})

		new_offer = JobOffer.objects.create(
			created_by=request.user,
			company_name=form_data['name'],
			title=form_data['title'],
			description=form_data['description'],
			location=form_data['location'],
			salary_range=form_data['salary_range'],
		)

		messages.success(request, 'La oferta de empleo se creo correctamente.')
		return redirect('jobs:job_detail', job_id=new_offer.pk)

	return render(request, 'jobs/create_job_offer.html', {'form_data': form_data})


@login_required
@require_POST
def apply_offer(request, job_id):
	offer = get_object_or_404(JobOffer, pk=job_id)

	if offer.created_by_id == request.user.id:
		messages.info(request, 'No puedes postularte a una oferta creada por tu propia cuenta.')
		return redirect('jobs:job_detail', job_id=offer.pk)

	application, created = JobApplication.objects.get_or_create(
		offer=offer,
		applicant=request.user,
	)

	if created:
		messages.success(request, 'Te postulaste correctamente a la oferta.')
	else:
		messages.info(request, 'Ya te habias postulado a esta oferta.')

	return redirect('jobs:job_detail', job_id=offer.pk)


@login_required
@require_POST
def delete_offer(request, job_id):
	if not _is_company_user(request.user):
		messages.error(request, 'Solo una cuenta empresa puede eliminar ofertas de empleo.')
		return redirect('jobs:job_list')

	offer = get_object_or_404(JobOffer, pk=job_id)

	if offer.created_by_id != request.user.id:
		messages.error(request, 'No tienes permisos para eliminar esta oferta.')
		return redirect('jobs:company_job_list')

	offer.delete()
	messages.success(request, 'Oferta eliminada correctamente.')
	return redirect('jobs:company_job_list')
