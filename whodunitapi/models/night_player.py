from django.db import models

class NightPlayer(models.Model):
    """Join model for Movie_nights and Players
    """
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    movie_night = models.ForeignKey("MovieNight", on_delete=models.CASCADE)