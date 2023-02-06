from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='Games')
    description = models.Charfield(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='Gamers')