from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):

    def retrieve(self, request, pk):

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        events = Event.objects.all()

        # if request.auth.user.is_staff:
        #     events = Event.objects.all()

        #     if "game" in request.query_params:
        #         if request.query_params['game'] == 1:
        #             events = events.filter(date_completed__isnull=False)

        #     if request.query_params['game'] == "all":
        #         pass

        # else:
        #     events = Event.objects.filter(gamer_user=request.auth.user)
        gamer = Gamer.objects.get(user=request.auth.user)
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
            
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        # gamer = Gamer.objects.get(user=request.auth.user)
        try: 
            game = Game.objects.get(pk=request.data['game_id'])
        except Game.DoesNotExist: 
            return Response({'message': "This game does not exist."}, status=status.HTTP_404_NOT_FOUND)

        event = Event.objects.create(
            description=request.data['description'],
            date=request.data['date'],
            time=request.data['time'],
            game=game
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            game = Game.objects.get(pk=request.data['game'])
        except Game.DoesNotExist:
            return Response({'message': 'You sent an invalid game ID'}, status=status.HTTP_404_NOT_FOUND)
            
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.time = request.data["time"]
        event.date = request.data["date"]
        # game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    #Action decorator turns a method into a new route
    @action(methods=['post'], detail=True) #Accepts POST & since detail=True, url will include PK
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True) #Accepts POST & since detail=True, url will include PK
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
# class EventGamerSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model = Gamer 
#         fields = ('full_name')

class EventSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Event 
        fields = ('id', 'description', 'date', 'time', 'game', 'attendees', 'joined', )
        depth = 2
