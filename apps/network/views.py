from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import ConnectionRequest
from apps.posts.models import Publication
from apps.profiles.models import Education, UserWebSkill, WorkExperience


@login_required
def contacts(request):
    User = get_user_model()

    pending_requests = ConnectionRequest.objects.filter(
        receiver=request.user,
        status=ConnectionRequest.Status.PENDING,
    ).select_related('sender')

    accepted_pairs = ConnectionRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status=ConnectionRequest.Status.ACCEPTED,
    ).values_list('sender_id', 'receiver_id')

    connected_user_ids = set()
    for sender_id, receiver_id in accepted_pairs:
        if sender_id != request.user.id:
            connected_user_ids.add(sender_id)
        if receiver_id != request.user.id:
            connected_user_ids.add(receiver_id)

    pending_pairs = ConnectionRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status=ConnectionRequest.Status.PENDING,
    ).values_list('sender_id', 'receiver_id')

    pending_related_user_ids = set()
    for sender_id, receiver_id in pending_pairs:
        if sender_id != request.user.id:
            pending_related_user_ids.add(sender_id)
        if receiver_id != request.user.id:
            pending_related_user_ids.add(receiver_id)

    suggested_profiles = (
        User.objects.filter(is_active=True)
        .exclude(pk=request.user.pk)
        .exclude(pk__in=connected_user_ids)
        .exclude(pk__in=pending_related_user_ids)
        .order_by('-date_joined')[:9]
    )

    return render(
        request,
        'network/contacts.html',
        {
            'pending_requests': pending_requests,
            'suggested_profiles': suggested_profiles,
            'contacts_count': len(connected_user_ids),
            'pending_count': pending_requests.count(),
        },
    )


@login_required
def contact_profile(request, username):
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username, is_active=True)
    connected = ConnectionRequest.objects.filter(
        (
            Q(sender=request.user, receiver=profile_user) |
            Q(sender=profile_user, receiver=request.user)
        ),
        status=ConnectionRequest.Status.ACCEPTED,
    ).exists()
    pending_sent = ConnectionRequest.objects.filter(
        sender=request.user,
        receiver=profile_user,
        status=ConnectionRequest.Status.PENDING,
    ).exists()

    context = {
        'profile_user': profile_user,
        'current_user_display_name': str(profile_user),
        'current_user_username': profile_user.username,
        'current_user_role': profile_user.get_tipoUsuario_display() if hasattr(profile_user, 'get_tipoUsuario_display') else 'Cuenta personal',
        'recent_publications': Publication.objects.filter(author=profile_user).select_related('author')[:5],
        'work_experiences': WorkExperience.objects.filter(user=profile_user),
        'educations': Education.objects.filter(user=profile_user),
        'selected_user_skills': UserWebSkill.objects.filter(user=profile_user).select_related('skill'),
        'is_own_profile': profile_user.pk == request.user.pk,
        'is_connected': connected,
        'pending_sent': pending_sent,
    }
    return render(request, 'profiles/contact_profile.html', context)


@login_required
@require_POST
def send_connection_request(request, username):
    User = get_user_model()
    receiver = get_object_or_404(User, username=username)

    if receiver.pk == request.user.pk:
        messages.error(request, 'No puedes conectarte contigo mismo.')
        return redirect(request.POST.get('next') or 'profiles:my_profile')

    relation, created = ConnectionRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status': ConnectionRequest.Status.PENDING},
    )

    if created:
        messages.success(request, 'Solicitud de conexion enviada.')
    elif relation.status == ConnectionRequest.Status.PENDING:
        messages.info(request, 'Ya enviaste una solicitud a este perfil.')
    elif relation.status == ConnectionRequest.Status.ACCEPTED:
        messages.info(request, 'Ya estan conectados.')
    else:
        relation.status = ConnectionRequest.Status.PENDING
        relation.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Solicitud de conexion reenviada.')

    return redirect(request.POST.get('next') or 'profiles:my_profile')


@login_required
@require_POST
def accept_connection_request(request, request_id):
    connection_request = get_object_or_404(
        ConnectionRequest,
        pk=request_id,
        receiver=request.user,
        status=ConnectionRequest.Status.PENDING,
    )
    connection_request.status = ConnectionRequest.Status.ACCEPTED
    connection_request.save(update_fields=['status', 'updated_at'])
    messages.success(request, 'Solicitud aceptada.')
    return redirect('network:contacts')


@login_required
@require_POST
def reject_connection_request(request, request_id):
    connection_request = get_object_or_404(
        ConnectionRequest,
        pk=request_id,
        receiver=request.user,
        status=ConnectionRequest.Status.PENDING,
    )
    connection_request.status = ConnectionRequest.Status.REJECTED
    connection_request.save(update_fields=['status', 'updated_at'])
    messages.info(request, 'Solicitud rechazada.')
    return redirect('network:contacts')
