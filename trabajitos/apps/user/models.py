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
    title = models.TextField()
    company = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User)
    
    class Meta:
        unique_together = (('url', 'user',),('siteid', 'user',))
        
class Account(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="model", null=True, blank=True)
    
class Alert(models.Model):
    provinces = models.CharField(max_length=500)
    words = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    
class JobAlert(models.Model):
    alert = models.ForeignKey(Alert)
    date = models.DateField(auto_now=True, auto_now_add=True)
    time = models.TimeField(auto_now=True, auto_now_add=True)
    url = models.CharField(max_length=255)
    siteid = models.CharField(max_length=255)
    title = models.TextField()
    company = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User)