from django.db import models

# Create your models here.

class product(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    stock = models.IntegerField(default=0,null=True,blank=True)
    price = models.DecimalField(default=0.00,null=True,blank=True,decimal_places=2,max_digits=10)

    def __str__(self):
        return self.name
