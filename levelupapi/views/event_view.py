from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


class EventView(ViewSet): 

    def retrieve(self, request, pk): 

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event) 
        return Response(serializer.data) 

    def list(self, request): 

        events = Event.objects.all()

        # if request.auth.user.is_staff:
        #     events = Event.objects.all()
        # else:
        #     events = Event.objects.filter(gamer__user=request.auth.user)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Event 
        fields = ('id', 'description', 'date', 'time', 'game', )
        depth = 1
