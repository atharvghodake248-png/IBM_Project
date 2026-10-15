from django.contrib.auth.models import User
from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    lat = models.CharField(max_length=30, blank=True)
    long = models.CharField(max_length=30, blank=True)
    short_name = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    dealer = models.ForeignKey(
        Dealer, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    purchase = models.CharField(max_length=100, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dealer} - {self.rating}/5"
