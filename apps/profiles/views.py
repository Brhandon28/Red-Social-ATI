from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _


def my_profile(request):
    return render(request, 'profiles/my_profile.html')


def edit_profile(request):
    if request.method == 'POST':
        messages.success(request, _('Tu perfil fue actualizado exitosamente.'))
        return redirect('profiles:my_profile')
    return render(request, 'profiles/edit_profile.html')


def contact_profile(request, username):
    return render(request, 'profiles/contact_profile.html', {'username': username})
