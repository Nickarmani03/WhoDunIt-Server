from django.db import models
from django.contrib.auth.models import User  # pylint:disable=(imported-auth-user)


class Players(models.Model):
    """players Model
    Args:
        models (OneToOneField): The user information for the players
        bio (CharField): The bio of the user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.ImageField(upload_to="image", null=True)