# # posts/views.py
# from django.shortcuts import render
# from django.http import HttpResponse

# def feed(request):
#     return HttpResponse("¡Feed funcionando!")

# posts/views.py

from django.shortcuts import render


def feed(request):
    return render(request, 'posts/feed.html')