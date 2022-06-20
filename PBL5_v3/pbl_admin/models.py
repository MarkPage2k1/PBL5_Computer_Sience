from distutils.command.upload import upload
from django.db import models
from numpy import True_

# Create your models here.
class Device(models.Model):
    name = models.TextField(max_length=255)
    image = models.ImageField(blank=True)
    cost = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __init__(self, name=None, image=None, cost=0, total=0):
        super().__init__()
        name = self.name
        image = self.image
        cost = self.cost
        total = self.total

    def __str__(self) -> str:
        return f'{self.name} {self.image} {self.cost} {self.total}'
    
    
