from django.db import models

# Create your models here.
class Device(models.Model):
    name = models.TextField(max_length=255)
    cost = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    def __init__(self, name=None, cost=0, count=0):
        super().__init__()
        name = self.name
        cost = self.cost
        count = self.count
    
    
