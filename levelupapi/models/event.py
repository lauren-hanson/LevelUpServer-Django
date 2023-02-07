from django.db import models

class Event(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='event_games')
    description = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    gamer = models.ManyToManyField("Gamer", through="EventGamer")