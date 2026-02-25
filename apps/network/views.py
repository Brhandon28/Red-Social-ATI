from django.shortcuts import render


def contacts(request):
    return render(request, 'network/contacts.html')


def contact_profile(request, username):
    return render(request, 'profiles/contact_profile.html', {'username': username})
