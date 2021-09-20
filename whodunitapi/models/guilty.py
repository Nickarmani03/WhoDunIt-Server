from django.db import models

class Guilty(models.Model):
    """Guilty model
    fields:
        label (CharField): name of the type of guilty
    """
    label = models.CharField(max_length=50)