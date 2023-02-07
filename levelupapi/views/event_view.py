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
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Event 
        fields = ('id', 'description', 'date', 'time', 'game')