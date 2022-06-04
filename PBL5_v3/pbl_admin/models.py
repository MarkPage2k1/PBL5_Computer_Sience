from django.db import models

# Create your models here.
class Device(models.Model):
    name = models.TextField(max_length=255)
    image = models.TextField(default='Image Devices')
    cost = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __init__(self, name=None, image=None, cost=0, total=0):
        super().__init__()
        name = self.name
        image = self.image
        cost = self.cost
        total = self.total
    
    
