from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
from rest_framework.decorators import list_route

from .models import Game
from .serializers import GameSerializer
from .utils import *
# Create your views here.


def assign(request):
    userid = request.GET.get('userid')
    if request.method == 'GET':
        gameid, weight = get_game(userid)
        data = {"gameid" : gameid, "weight" : weight}
        serializer = GameSerializer(data)
        return JsonResponse(serializer.data, safe=False)
