from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    price = models.FloatField()
    img_url = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=60, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    isactive = models.BooleanField(default=True)


class Biding(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, to_field='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    bid = models.IntegerField()

class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, to_field='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, to_field='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')