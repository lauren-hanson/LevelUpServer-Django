from django.db import models
from django.contrib.auth.models import User


class EventGamer(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='Games')
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='Events')