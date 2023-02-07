from django.db import models

class GameType(models.Model):

    label = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='label_game_types')