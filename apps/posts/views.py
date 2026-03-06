# # posts/views.py
# from django.shortcuts import render
# from django.http import HttpResponse

# def feed(request):
#     return HttpResponse("¡Feed funcionando!")

# posts/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def feed(request):
    return render(request, 'posts/feed.html')