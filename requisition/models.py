from django.db import models
from django.utils. timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Requisition(models.Model):
    sent_date = models.DateField(default=now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    department = models.CharField( max_length=50, default='department')
    item = models.CharField(max_length=50, default='item')
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    seller_name = models.CharField( max_length=50, default='name')
    seller_address = models.CharField( max_length=50, default='address')
    price = models.IntegerField(default=1)
    accepted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False) 
    rejected = models.BooleanField(default=False) 
    


    def __str__(self):
        return str(self.owner)
    
    class Meta:
        ordering = ["-sent_date"]


    

