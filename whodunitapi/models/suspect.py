from django.db import models


class Suspect(models.Model):
    """Movie Model
    Fields:
        name (CharField): The name of the suspect        
        description (CharField): The description of the movie
        is_guilty (BooleanField): the suspected criminal is guilty or not
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    is_guilty = models.BooleanField()