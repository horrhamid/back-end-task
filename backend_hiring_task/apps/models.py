from django.db import models
from picklefield.fields import PickledObjectField
# Create your models here.


class Apps(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=1000)
    command = models.CharField(max_length=1000)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Dicty(models.Model):
    key = models.CharField(max_length=250, null=True)
    value = models.CharField(max_length=250, null=True)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE, related_name='envs', null=True)

    def __str__(self):
        return self.key
