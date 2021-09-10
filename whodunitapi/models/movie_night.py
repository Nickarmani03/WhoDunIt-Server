from django.db import models


class MovieNight(models.Model):
    """MovieNight Model
    Fields:
        creator (ForeignKey): the user that made the Movie Night
        movie (ForeignKey): the movie associated with the Movie Night
        date (DateField): The date of the Movie Night
        time (TimeFIeld): The time of the Movie Night
        title (CharField): The title of the Movie Night
        description (TextField): The description of the Movie Night        
        attendees (ManyToManyField): The movie watchers attending the Movie Night
    """
    creator = models.ForeignKey("Player", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=1000)
    description = models.TextField()    
    attendees = models.ManyToManyField("Player", through="MovieNight", related_name="attending")
    # this is a list