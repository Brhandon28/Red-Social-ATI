from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

SAMPLE_PUBLICATIONS = [
    {
        'id': 1,
        'company': 'Empresa',
        'followers': '326 followers',
        'age': '18 h',
        'summary': (
            'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac '
            'sapien enim nulla tellus risus ornare lobortis commodo in proin in fermentum morbi at sem '
            'facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus '
            'ipsum nec nibh lacus, suspendisse'
        ),
    },
    {
        'id': 2,
        'company': 'Company name',
        'followers': '326 followers',
        'age': '20 h',
        'summary': (
            'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac '
            'sapien enim nulla tellus risus ornare lobortis commodo in proin in fermentum morbi at sem '
            'facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus.'
        ),
    },
    {
        'id': 3,
        'company': 'Company name',
        'followers': '326 followers',
        'age': '20 h',
        'summary': (
            'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac '
            'sapien enim nulla tellus risus ornare lobortis commodo in proin ........'
        ),
    },
    {
        'id': 4,
        'company': 'Company name',
        'followers': '326 followers',
        'age': '20 h',
        'summary': (
            'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac '
            'sapien enim nulla tellus risus ornare lobortis commodo in proin ........'
        ),
    },
]

SAMPLE_COMMENTS = [
    {
        'id': 1,
        'author': 'Maecenas condimentum',
        'text': (
            'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac '
            'sapien enim nulla tellus risus ornare lobortis commodo in proin in fermentum morbi at sem '
            'facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus '
            'ipsum nec nibh lacus, suspendisse'
        ),
    },
    {
        'id': 2,
        'author': 'Maecenas condimentum',
        'text': (
            'Lacus amet, laoreet viverra id faucibus nisi cras est sit pellentesque amet in auctor ac '
            'sapien enim nulla tellus risus ornare lobortis commodo in proin in fermentum morbi at sem '
            'facilisi orci magna in sagittis, tortor ac maecenas eget etiam ullamcorper magna eu risus '
            'ipsum nec nibh lacus, suspendisse'
        ),
    },
]


def _get_current_user_profile(request):
    user = request.user
    if user.is_authenticated:
        return {
            'display_name': str(user),
            'role': 'Cuenta personal',
        }
    return {
        'display_name': 'Usuario',
        'role': 'Cuenta personal',
    }


def _get_session_publications(request):
    return request.session.get('publications_created', [])


def _save_session_publications(request, publications):
    request.session['publications_created'] = publications


def _build_publications_for_ui(request):
    return _get_session_publications(request) + SAMPLE_PUBLICATIONS


def _next_publication_id(publications):
    if not publications:
        return 1
    return max(publication['id'] for publication in publications) + 1


def _get_publication(post_id, publications):
    return next((publication for publication in publications if publication['id'] == post_id), publications[0])


@login_required
def index(request):
    user_profile = _get_current_user_profile(request)
    publications = _build_publications_for_ui(request)

    return render(
        request,
        'feed/index.html',
        {
            'publications': publications,
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )


@login_required
def company_feed(request):
    user_profile = _get_current_user_profile(request)
    publications = _build_publications_for_ui(request)

    return render(
        request,
        'feed/company_feed.html',
        {
            'publications': publications[:2],
            'top_publications': publications[1:4],
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )


@login_required
def post_detail(request, post_id):
    publications = _build_publications_for_ui(request)
    publication = _get_publication(post_id, publications)
    top_publications = [item for item in publications if item['id'] != publication['id']][:3]

    return render(
        request,
        'feed/publication_detail.html',
        {
            'publication': publication,
            'comments': SAMPLE_COMMENTS,
            'top_publications': top_publications,
        },
    )


@login_required
def create_post(request):
    user_profile = _get_current_user_profile(request)

    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()

        if not content:
            messages.error(request, _('Escribe el contenido de la publicación antes de publicar.'))
            return render(
                request,
                'posts/create_post.html',
                {
                    'current_user_display_name': user_profile['display_name'],
                    'current_user_role': user_profile['role'],
                },
            )

        publications_for_ui = _build_publications_for_ui(request)
        new_publication = {
            'id': _next_publication_id(publications_for_ui),
            'company': user_profile['display_name'],
            'followers': user_profile['role'],
            'age': 'Ahora',
            'summary': content,
        }

        session_publications = _get_session_publications(request)
        session_publications.insert(0, new_publication)
        _save_session_publications(request, session_publications)

        messages.success(request, _('Tu publicación fue creada exitosamente.'))
        return redirect('feed:index')

    return render(
        request,
        'posts/create_post.html',
        {
            'current_user_display_name': user_profile['display_name'],
            'current_user_role': user_profile['role'],
        },
    )
