from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def push_redis(request):
    room_name = request.GET.get('room')

    def push(msg):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room_name,
            {
                "type": "tui.song",
                'msg': msg
            }
        )

    push('推送测试！')
    return JsonResponse({'1': 1})
