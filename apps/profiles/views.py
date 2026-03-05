from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _


@login_required
def my_profile(request):
    user = request.user
    display_name = str(user) if user.is_authenticated else 'Usuario'
    username = user.username if user.is_authenticated else 'usuario'

    return render(
        request,
        'profiles/my_profile.html',
        {
            'current_user_display_name': display_name,
            'current_user_username': username,
            'current_user_role': 'Cuenta personal',
        },
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        messages.success(request, _('Tu perfil fue actualizado exitosamente.'))
        return redirect('profiles:my_profile')
    return render(request, 'profiles/edit_profile.html')


@login_required
def contact_profile(request, username):
    return render(request, 'profiles/contact_profile.html', {'username': username})
