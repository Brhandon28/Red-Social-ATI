from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def contacts(request):
    return render(request, 'network/contacts.html')


@login_required
def contact_profile(request, username):
    return render(request, 'profiles/contact_profile.html', {'username': username})
