from django.db import models

class Genre(models.Model):
    """Genre model
    fields:
        label (CharField): name of the type of genre
    """
    label = models.CharField(max_length=50)