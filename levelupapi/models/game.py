from django.db import models

class Game(models.Model):

    title = models.CharField(max_length=100)
    maker = models.CharField(max_length=100)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='label_gametype')
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='game_gamer')
    num_of_players = models.IntegerField()
    skill_level = models.IntegerField()