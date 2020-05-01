from django.db import models
from django.contrib.auth.models import User
from accounts.models import Client,Employee
# Create your models here.
SALARY_TYPE = (
	("MONTHLY", "MONTHLY"),
	("HOURLY", "HOURLY"),
	)


class Salarie(models.Model):
    user = models.ForeignKey(Employee,on_delete=models.CASCADE,blank=True,null=True)
    type = models.CharField(max_length=10,choices=SALARY_TYPE)
    amount = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.user.name
class Invoice(models.Model):
    order_id = models.CharField(max_length=15) #,unique=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    service = models.CharField(max_length=50,blank=True,null=True)
    stylist = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=50, blank=True, null=True)
    bill = models.CharField(max_length=10, null=True, blank=True, default=0.00)
    
    def __str__(self):
        try:
            return self.order_id + " " +self.name + " "+ str(self.email) 
        except:
            return self.order_id + " " + self.name
    
    