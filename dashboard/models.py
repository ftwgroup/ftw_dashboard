from django.db import models

class Pitch(models.Model):
    snippet = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="images/pitch")
