from django.db import models


class Event(models.Model):
    """Event Model
    Fields:
        host (ForeignKey): the user that made the event
        movie
 (ForeignKey): the movie
 associated with the event
        date (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (TextField): The text description of the event
        title (CharField): The title of the event
        attendees (ManyToManyField): The movie
rs attending the event
    """
    creator = models.ForeignKey("Player", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=1000)
    description = models.TextField()    
    attendees = models.ManyToManyField("Player", through="EventMovier", related_name="attending")
    # this is a list