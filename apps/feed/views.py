from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import BooleanField, Count, Exists, OuterRef, Q, Value
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.posts.models import Comment, CommentLike, Publication, PublicationLike
from apps.network.models import ConnectionRequest


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


def _safe_next_url(request, default_url):
    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
        return next_url
    return default_url


def _publication_queryset_for_user(user):
    publications = Publication.objects.select_related('author').annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True),
    )

    if user.is_authenticated:
        return publications.annotate(
            liked_by_me=Exists(
                PublicationLike.objects.filter(publication=OuterRef('pk'), user=user)
            )
        ).order_by('-created_at')

    return publications.annotate(liked_by_me=Value(False, output_field=BooleanField())).order_by('-created_at')


def _comment_queryset_for_user(publication, user, *, top_level_only=False, replies_only=False):
    comments = Comment.objects.filter(publication=publication).select_related('author').annotate(
        likes_count=Count('likes', distinct=True),
    )

    if top_level_only:
        comments = comments.filter(parent__isnull=True)
    if replies_only:
        comments = comments.filter(parent__isnull=False)

    if user.is_authenticated:
        comments = comments.annotate(
            liked_by_me=Exists(CommentLike.objects.filter(comment=OuterRef('pk'), user=user))
        )
    else:
        comments = comments.annotate(liked_by_me=Value(False, output_field=BooleanField()))

    return comments.order_by('created_at')


def _top_publications_for_user(user, limit=3):
    return _publication_queryset_for_user(user).order_by('-likes_count', '-comments_count', '-created_at')[:limit]


def _contacts_count_for_user(user):
    if not user.is_authenticated:
        return 0

    accepted_pairs = ConnectionRequest.objects.filter(
        Q(sender=user) | Q(receiver=user),
        status=ConnectionRequest.Status.ACCEPTED,
    ).values_list('sender_id', 'receiver_id')

    connected_user_ids = set()
    for sender_id, receiver_id in accepted_pairs:
        if sender_id != user.id:
            connected_user_ids.add(sender_id)
        if receiver_id != user.id:
            connected_user_ids.add(receiver_id)

    return len(connected_user_ids)


@login_required
def index(request):
    user_profile = _get_current_user_profile(request)
    publications = _publication_queryset_for_user(request.user)
    top_publications = _top_publications_for_user(request.user)

    return render(
        request,
        'feed/index.html',
        {
            'publications': publications,
            'top_publications': top_publications,
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )


@login_required
def company_feed(request):
    if not _is_company_user(request.user):
        messages.error(request, _('Esta seccion esta disponible solo para cuentas empresa.'))
        return redirect('feed:index')

    user_profile = _get_current_user_profile(request)
    publications = _publication_queryset_for_user(request.user)

    return render(
        request,
        'feed/company_feed.html',
        {
            'publications': publications[:2],
            'top_publications': publications.order_by('-likes_count', '-created_at')[:3],
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )


@login_required
def post_detail(request, post_id):
    publication = get_object_or_404(_publication_queryset_for_user(request.user), pk=post_id)
    comments = list(_comment_queryset_for_user(publication, request.user, top_level_only=True))
    replies = _comment_queryset_for_user(publication, request.user, replies_only=True)
    replies_by_parent = {}
    for reply in replies:
        replies_by_parent.setdefault(reply.parent_id, []).append(reply)
    for comment in comments:
        comment.replies_for_ui = replies_by_parent.get(comment.id, [])

    top_publications = (
        _publication_queryset_for_user(request.user)
        .exclude(pk=publication.pk)
        .order_by('-likes_count', '-created_at')[:3]
    )

    return render(
        request,
        'feed/publication_detail.html',
        {
            'publication': publication,
            'comments': comments,
            'top_publications': top_publications,
        },
    )


@login_required
def create_post(request):
    user_profile = _get_current_user_profile(request)
    top_publications = _top_publications_for_user(request.user)
    current_user_contacts_count = _contacts_count_for_user(request.user)

    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        image = request.FILES.get('image')

        if not content and not image:
            messages.error(request, _('Escribe el contenido de la publicación antes de publicar.'))
            return render(
                request,
                'posts/create_post.html',
                {
                    'current_user_display_name': user_profile['display_name'],
                    'current_user_role': user_profile['role'],
                    'current_user_contacts_count': current_user_contacts_count,
                    'top_publications': top_publications,
                },
            )

        Publication.objects.create(author=request.user, content=content, image=image)

        messages.success(request, _('Tu publicación fue creada exitosamente.'))
        return redirect('feed:index')

    return render(
        request,
        'posts/create_post.html',
        {
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
            'current_user_contacts_count': current_user_contacts_count,
            'top_publications': top_publications,
        },
    )


@login_required
@require_POST
def add_comment(request, post_id):
    publication = get_object_or_404(Publication, pk=post_id)
    content = (request.POST.get('content') or '').strip()
    parent_comment_id = request.POST.get('parent_comment_id')

    if not content:
        messages.error(request, _('Escribe un comentario antes de publicarlo.'))
        return redirect('feed:publication_detail', post_id=publication.pk)

    parent_comment = None
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, pk=parent_comment_id, publication=publication)

    Comment.objects.create(
        publication=publication,
        parent=parent_comment,
        author=request.user,
        content=content,
    )
    messages.success(request, _('Tu comentario fue publicado.'))
    return redirect('feed:publication_detail', post_id=publication.pk)


@login_required
@require_POST
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, publication_id=post_id)

    if comment.author_id != request.user.id:
        messages.error(request, _('No tienes permisos para editar este comentario.'))
        return redirect('feed:publication_detail', post_id=post_id)

    content = (request.POST.get('content') or '').strip()
    if not content:
        messages.error(request, _('El comentario no puede quedar vacio.'))
        return redirect(f"{_safe_next_url(request, f'/feed/publicacion/{post_id}/')}?edit_comment={comment_id}")

    comment.content = content
    comment.save(update_fields=['content', 'updated_at'])
    messages.success(request, _('Comentario actualizado correctamente.'))

    default_url = request.META.get('HTTP_REFERER') or f'/feed/publicacion/{post_id}/'
    return redirect(_safe_next_url(request, default_url))


@login_required
@require_POST
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, publication_id=post_id)

    if comment.author_id != request.user.id:
        messages.error(request, _('No tienes permisos para eliminar este comentario.'))
        return redirect('feed:publication_detail', post_id=post_id)

    comment.delete()
    messages.success(request, _('Comentario eliminado.'))

    default_url = request.META.get('HTTP_REFERER') or f'/feed/publicacion/{post_id}/'
    return redirect(_safe_next_url(request, default_url))


@login_required
@require_POST
def toggle_publication_like(request, post_id):
    publication = get_object_or_404(Publication, pk=post_id)
    like, created = PublicationLike.objects.get_or_create(
        publication=publication,
        user=request.user,
    )

    if not created:
        like.delete()

    default_url = request.META.get('HTTP_REFERER') or '/feed/'
    return redirect(_safe_next_url(request, default_url))


@login_required
@require_POST
def delete_publication(request, post_id):
    publication = get_object_or_404(Publication, pk=post_id)

    if publication.author_id != request.user.id:
        messages.error(request, _('No tienes permisos para eliminar esta publicacion.'))
        return redirect('feed:publication_detail', post_id=post_id)

    publication.delete()
    messages.success(request, _('Publicacion eliminada.'))

    default_url = request.META.get('HTTP_REFERER') or '/feed/'
    return redirect(_safe_next_url(request, default_url))


@login_required
@require_POST
def toggle_comment_like(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, publication_id=post_id)
    like, created = CommentLike.objects.get_or_create(
        comment=comment,
        user=request.user,
    )

    if not created:
        like.delete()

    default_url = request.META.get('HTTP_REFERER') or f'/feed/publicacion/{post_id}/'
    return redirect(_safe_next_url(request, default_url))
