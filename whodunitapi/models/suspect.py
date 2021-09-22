from django.db import models


class Suspect(models.Model):
    """Movie Model
    Fields:
        name (CharField): The name of the suspect        
        description (CharField): The description of the movie
        guilty (ForeignKey): the suspected criminal is guilty or not
        movie (ForeignKey): the suspected criminal's movie they are in.
        suspect_image_url (CharField): for the user to upload an image.
    """
    name = models.CharField(max_length=100)    
    guilty = models.ForeignKey("Guilty", on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    suspect_image_url = models.CharField(max_length=255)