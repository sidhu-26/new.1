

from django.db import models


class Gym(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    distance = models.IntegerField()

    def __str__(self):
        return self.name
