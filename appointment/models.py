from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    price = models.DecimalField(max_digits=10,default=0.00,decimal_places=2)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    service = models.CharField(max_length=50,null=True,blank=True)
    contact = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    time = models.CharField(max_length=10,blank=True,null=True)
    note = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name + " " + str(self.email) + " " +str(self.contact)

class Complain(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name + " " + str(self.email)



