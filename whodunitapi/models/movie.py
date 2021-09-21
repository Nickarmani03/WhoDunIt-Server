from django.db import models


class Movie(models.Model):
    """Movie Model
    Fields:
        name (CharField): The name of the movie
        year (IntegerField): the year the movie debuted
        description (CharField): The description of the movie
        genre (ForeignKey): The type of genre of the movie
        number_of_players (IntegerField): The max number of players watching the movie
        director (CharField): The person that made the movie
        rating (CharField): the movies rating
        # suspect (ForeignKey): the suspected criminal
        movie_image_url (CharField): for the user to upload an image.
    """
    name = models.CharField(max_length=100)
    year = models.IntegerField()    
    description = models.CharField(max_length=1000)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()    
    director = models.CharField(max_length=50)
    rating = models.CharField(max_length=6)
    # suspect = models.ForeignKey("Suspect", on_delete=models.CASCADE)
    movie_image_url = models.CharField(max_length=255)
    
    # @property
    # def movie_suspect(self):
    #     suspect = Suspect.objects.filter(movie=self)