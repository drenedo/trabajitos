from django.db import models
from django.contrib.auth.models import User

class Search(models.Model):
    provinces = models.CharField(max_length=500)
    words = models.CharField(max_length=500)
    non = models.CharField(max_length=500)
    locations = models.CharField(max_length=500)
    user = models.ForeignKey(User)

class Find(models.Model):
    search = models.ForeignKey(Search)
    date = models.DateField(auto_now=True, auto_now_add=True)
    time = models.TimeField(auto_now=True, auto_now_add=True)
    total = models.IntegerField()
    efective = models.IntegerField()
    
class Job(models.Model):
    find = models.ForeignKey(Find)
    status = models.IntegerField()
    url = models.CharField(max_length=255)
    siteid = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    class Meta:
        unique_together = (('url', 'user',),('siteid', 'user',))