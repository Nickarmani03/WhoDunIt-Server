from django.db import models
from django.contrib.auth.models import User #pylint:disable=(imported-auth-user)


class Player(models.Model):
    """player Model
    Args:
        user (OneToOneField): The user information for the player
        bio (CharField): The bio of the user
        profile_image_url (CharField): for the user to upload an image.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url= models.CharField(max_length=255)

    # def __str__(self):
    #     return self.name + ": " + str(self.imagefile)
    