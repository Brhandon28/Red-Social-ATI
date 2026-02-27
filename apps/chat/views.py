from django.shortcuts import render


def inbox(request):
    return render(request, 'chat/inbox.html')


def chat_detail(request, chat_id):
    return render(request, 'chat/chat_detail.html', {'chat_id': chat_id})
