from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def inbox(request):
    return render(request, 'chat/inbox.html')


@login_required
def chat_detail(request, chat_id):
    return render(request, 'chat/chat_detail.html', {'chat_id': chat_id})
