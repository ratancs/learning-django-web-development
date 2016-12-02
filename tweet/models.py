from django.db import models

from user_profile.models import User


class Tweet(models.Model):
    """
    	Tweet model
    """
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, default="Global")
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.text


class HashTag(models.Model):
    """
    	HashTag model
    """
    name = models.CharField(max_length=64, unique=True)
    tweet = models.ManyToManyField(Tweet)

    def __unicode__(self):
        return self.name
