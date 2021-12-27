from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=15, decimal_places=5)
    lon = models.DecimalField(max_digits=15, decimal_places=5)
    class Meta:
        unique_together = ('lat', 'lon')
  
    def __str__(self):
        return f"{self.city}, {self.country}"

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    categories = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)
    api_id = models.CharField(max_length=255,unique=True)
    location = models.ForeignKey(Location, related_name="restaurants", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Attraction(models.Model):
    name = models.CharField(max_length=255)
    api_id = models.CharField(max_length=255, unique=True)
    kinds = models.CharField(max_length=255, blank=True)
    location = models.ForeignKey(Location, related_name="attractions", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MyLocation(models.Model):
    traveller = models.ForeignKey(User, related_name="my_locations", on_delete=models.CASCADE )
    location = models.ForeignKey(Location, related_name="my_locations", on_delete=models.CASCADE)
    restaurants = models.ManyToManyField(Restaurant, related_name="my_locations", blank=True)
    attractions = models.ManyToManyField(Attraction, related_name="my_locations", blank=True)

    class Meta:
        unique_together = ('traveller', 'location')

    def __str__(self):
        return f"{self.location} by {self.traveller.username}"


    




