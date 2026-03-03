from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _


def my_profile(request):
    current_username = (getattr(request, 'hardcoded_user', '') or '').strip()
    if current_username:
        display_name = current_username.capitalize()
        username = current_username
    else:
        display_name = 'Usuario'
        username = 'usuario'

    return render(
        request,
        'profiles/my_profile.html',
        {
            'current_user_display_name': display_name,
            'current_user_username': username,
            'current_user_role': 'Cuenta personal',
        },
    )


def edit_profile(request):
    if request.method == 'POST':
        messages.success(request, _('Tu perfil fue actualizado exitosamente.'))
        return redirect('profiles:my_profile')
    return render(request, 'profiles/edit_profile.html')


def contact_profile(request, username):
    return render(request, 'profiles/contact_profile.html', {'username': username})
