from django.db import models
from django.contrib.auth.models import User


class GameType(models.Model):

    label = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='GameTypes')