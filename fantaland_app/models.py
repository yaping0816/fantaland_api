from django.db import models
from django.contrib.auth.models import User

class LocationList(models.Model):
    list_name = models.CharField(max_length=255)
    traveller = models.ForeignKey(User, related_name="location_lists", on_delete=models.CASCADE )

    def __str__(self):
        return f"{self.list_name} by {self.traveller.username}"


class Location(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=12)
    image = models.ImageField(blank=True)
    list = models.ForeignKey(LocationList, related_name="locations", on_delete=models.CASCADE)
  
    def __str__(self):
        return f"{self.city}, {self.state}"


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=255)
    cuisine_type = models.TextField()
    list = models.ForeignKey(LocationList, on_delete=models.CASCADE, related_name="restaurants", null=True, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.restaurant_name


class Attraction(models.Model):
    attraction_name = models.CharField(max_length=255)
    list = models.ForeignKey(LocationList, on_delete=models.CASCADE, related_name="attractions", null=True, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.attraction_name


    




