from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request, 'feed/index.html')


def post_detail(request, post_id):
    return render(request, 'feed/post_detail.html', {'post_id': post_id})


def create_post(request):
    if request.method == 'POST':
        messages.success(request, _('Tu publicación fue creada exitosamente.'))
        return redirect('feed:index')
    return render(request, 'feed/create_post.html')
