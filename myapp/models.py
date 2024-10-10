from django.db import models

# Create your models here.
class homedata(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    capacity = models.IntegerField()
    amenities = models.JSONField()  
    description = models.TextField()

    def __str__(self):
        return self.name