from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType

class GameView(ViewSet): 
    
    def retrieve(self, request, pk): 
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game) 
        return Response(serializer.data)

    def list(self, request): 
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request): 
        """Handle POST operations 
        
        Returns 
            Response -- JSON serialized game instance"""
        gamer = Gamer.objects.get(user=request.auth.user) 
        #declare gamer variable 
        #getting the user that is logged in based off token
        #request.auth.user is used to get the Gamer object based off the user

        game_type = GameType.objects.get(pk=request.data['game_type'])
        #declare game_type variable
        #retrieve GameType object from the database to verify the type the user is trying to add exists in the database
        #request.data holds the data passed in from the client. it must match what the client is passing to the server

        game = Game.objects.create(
            title=request.data['title'],
            maker=request.data['maker'],
            game_type=game_type,
            gamer=gamer,
            num_of_players=request.data['num_of_players'],
            skill_level=request.data['skill_level']
        )
        # declare game variable and call create ORM method & pass all field as parameters to the function

        serializer = GameSerializer(game)
        return Response(serializer.data)


class GameSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Game
        fields = ('id', 'title', 'maker', 'num_of_players', 'skill_level', 'game_type', 'gamer')