from django.db import models


class MovieSuspect(models.Model):
    """MovieSuspect Model
    Fields:
        player (ForeignKey): the user that made the Movie Suspect
        movie_night (ForeignKey): the movie associated with the Movie Night
        suspect (ForeignKey): the suspected criminal
        
    """

    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    movie_night = models.ForeignKey("MovieNight", on_delete=models.CASCADE)
    suspect = models.ForeignKey("Suspect", on_delete=models.CASCADE)
    