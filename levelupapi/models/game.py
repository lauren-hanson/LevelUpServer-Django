from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):

    title = models.Charfield(max_length=100)
    maker = models.Charfield(max_length=100)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='GameTypes')
    gamer = models.IntegerField()
    num_of_players = models.IntegerField()
    skill_level = models.IntegerField()