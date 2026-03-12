from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, IntegerField, Q, Value
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .models import Education, UserWebSkill, WebSkill, WorkExperience
from apps.network.models import ConnectionRequest
from apps.posts.models import Publication


DEFAULT_WEB_SKILLS = [
    'HTML',
    'CSS',
    'JavaScript',
    'TypeScript',
    'React',
    'Vue',
    'Angular',
    'Tailwind CSS',
    'Bootstrap',
    'Node.js',
    'Django',
    'Flask',
    'REST API',
    'GraphQL',
]


def _ensure_default_skills():
    for skill_name in DEFAULT_WEB_SKILLS:
        WebSkill.objects.get_or_create(
            name=skill_name,
            defaults={'is_system': True},
        )


def _role_label(user):
    if hasattr(user, 'get_tipoUsuario_display'):
        return user.get_tipoUsuario_display()
    return 'Cuenta personal'


def _profile_context(user):
    _ensure_default_skills()

    experiences = WorkExperience.objects.filter(user=user)
    educations = Education.objects.filter(user=user)
    selected_user_skills = UserWebSkill.objects.filter(user=user).select_related('skill')
    recent_publications = Publication.objects.filter(author=user).select_related('author')[:5]
    selected_skill_ids = [item.skill_id for item in selected_user_skills]

    User = get_user_model()
    suggestions_base = User.objects.filter(is_active=True).exclude(pk=user.pk)
    if selected_skill_ids:
        profile_suggestions = suggestions_base.annotate(
            shared_skills_count=Count(
                'user_web_skills',
                filter=Q(user_web_skills__skill_id__in=selected_skill_ids),
                distinct=True,
            )
        ).order_by('-shared_skills_count', '-date_joined')[:6]
    else:
        profile_suggestions = suggestions_base.annotate(
            shared_skills_count=Value(0, output_field=IntegerField())
        ).order_by('-date_joined')[:6]

    suggested_ids = [item.id for item in profile_suggestions]
    sent_request_user_ids = list(
        ConnectionRequest.objects.filter(
            sender=user,
            receiver_id__in=suggested_ids,
            status=ConnectionRequest.Status.PENDING,
        ).values_list('receiver_id', flat=True)
    )
    connected_pairs = list(
        ConnectionRequest.objects.filter(
            Q(sender=user, receiver_id__in=suggested_ids) |
            Q(receiver=user, sender_id__in=suggested_ids),
            status=ConnectionRequest.Status.ACCEPTED,
        )
        .values_list('sender_id', 'receiver_id')
    )
    connected_flat_ids = []
    for sender_id, receiver_id in connected_pairs:
        if sender_id != user.id:
            connected_flat_ids.append(sender_id)
        if receiver_id != user.id:
            connected_flat_ids.append(receiver_id)

    return {
        'profile_user': user,
        'current_user_display_name': str(user),
        'current_user_username': user.username,
        'current_user_role': _role_label(user),
        'recent_publications': recent_publications,
        'work_experiences': experiences,
        'educations': educations,
        'selected_user_skills': selected_user_skills,
        'available_skills': WebSkill.objects.exclude(id__in=selected_skill_ids),
        'profile_suggestions': profile_suggestions,
        'sent_request_user_ids': sent_request_user_ids,
        'connected_user_ids': connected_flat_ids,
    }


@login_required
def my_profile(request):
    return render(request, 'profiles/my_profile.html', _profile_context(request.user))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'basic')
        redirect_target = 'profiles:my_profile'

        if form_type == 'basic':
            request.user.first_name = (request.POST.get('first_name') or '').strip()
            request.user.last_name = (request.POST.get('last_name') or '').strip()
            request.user.email = (request.POST.get('email') or '').strip()
            request.user.nombreMostrado = (request.POST.get('nombreMostrado') or '').strip()
            profile_image = request.FILES.get('profileImage')
            banner_image = request.FILES.get('bannerImage')

            update_fields = ['first_name', 'last_name', 'email', 'nombreMostrado']
            if profile_image:
                request.user.profileImage = profile_image
                update_fields.append('profileImage')
            if banner_image:
                request.user.bannerImage = banner_image
                update_fields.append('bannerImage')

            request.user.save(update_fields=update_fields)
            messages.success(request, _('Tu perfil fue actualizado exitosamente.'))

        elif form_type == 'work_add':
            redirect_target = 'profiles:edit_profile'
            company = (request.POST.get('company') or '').strip()
            position = (request.POST.get('position') or '').strip()
            description = (request.POST.get('description') or '').strip()

            if not company or not position:
                messages.error(request, _('Completa empresa y cargo para agregar trayectoria laboral.'))
                return redirect('profiles:edit_profile')

            WorkExperience.objects.create(
                user=request.user,
                company=company,
                position=position,
                description=description,
            )
            messages.success(request, _('Trayectoria laboral agregada.'))

        elif form_type == 'work_delete':
            redirect_target = 'profiles:edit_profile'
            item_id = request.POST.get('item_id')
            work = WorkExperience.objects.filter(pk=item_id, user=request.user).first()
            if not work:
                messages.error(request, _('No se encontro la trayectoria laboral a eliminar.'))
            else:
                work.delete()
                messages.success(request, _('Trayectoria laboral eliminada.'))

        elif form_type == 'education_add':
            redirect_target = 'profiles:edit_profile'
            institution = (request.POST.get('institution') or '').strip()
            degree = (request.POST.get('degree') or '').strip()
            field_of_study = (request.POST.get('field_of_study') or '').strip()

            if not institution or not degree:
                messages.error(request, _('Completa institucion y titulo para agregar educacion.'))
                return redirect('profiles:edit_profile')

            Education.objects.create(
                user=request.user,
                institution=institution,
                degree=degree,
                field_of_study=field_of_study,
            )
            messages.success(request, _('Trayectoria educativa agregada.'))

        elif form_type == 'education_delete':
            redirect_target = 'profiles:edit_profile'
            item_id = request.POST.get('item_id')
            education = Education.objects.filter(pk=item_id, user=request.user).first()
            if not education:
                messages.error(request, _('No se encontro la trayectoria educativa a eliminar.'))
            else:
                education.delete()
                messages.success(request, _('Trayectoria educativa eliminada.'))

        elif form_type == 'skill_add_existing':
            redirect_target = 'profiles:edit_profile'
            skill_id = request.POST.get('skill_id')
            skill = WebSkill.objects.filter(pk=skill_id).first()
            if not skill:
                messages.error(request, _('Selecciona una habilidad valida.'))
                return redirect('profiles:edit_profile')

            try:
                UserWebSkill.objects.create(user=request.user, skill=skill)
                messages.success(request, _('Habilidad agregada a tu perfil.'))
            except IntegrityError:
                messages.info(request, _('Esa habilidad ya estaba en tu perfil.'))

        elif form_type == 'skill_add_new':
            redirect_target = 'profiles:edit_profile'
            new_skill_name = (request.POST.get('new_skill') or '').strip()
            if not new_skill_name:
                messages.error(request, _('Escribe el nombre de la nueva habilidad.'))
                return redirect('profiles:edit_profile')

            skill, created = WebSkill.objects.get_or_create(
                name=new_skill_name,
                defaults={
                    'created_by': request.user,
                    'is_system': False,
                },
            )

            try:
                UserWebSkill.objects.create(user=request.user, skill=skill)
                messages.success(request, _('Nueva habilidad creada y agregada a tu perfil.'))
            except IntegrityError:
                messages.info(request, _('La habilidad ya existe en tu perfil.'))

        elif form_type == 'skill_delete':
            redirect_target = 'profiles:edit_profile'
            item_id = request.POST.get('item_id')
            relation = UserWebSkill.objects.filter(pk=item_id, user=request.user).first()
            if not relation:
                messages.error(request, _('No se encontro la habilidad a eliminar.'))
            else:
                relation.delete()
                messages.success(request, _('Habilidad eliminada de tu perfil.'))

        return redirect(redirect_target)

    return render(request, 'profiles/edit_profile.html', _profile_context(request.user))


@login_required
def contact_profile(request, username):
    return redirect('network:contact_profile', username=username)
