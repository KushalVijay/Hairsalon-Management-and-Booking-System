from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)
    
    
    def get_name(self):
        return self.name + " , " + self.location

class Client(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)
    taxes = models.CharField(max_length=10,blank=True,null=True)
    leaves = models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return self.name+" "+str(self.user.email)

