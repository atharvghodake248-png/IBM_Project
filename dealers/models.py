from django.db import models
from django.contrib.auth.models import User

class Dealer(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
