from django.db import models

# Create your models here.

class PneumoniaDetail(models.Model):
    
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    image = models.CharField(max_length=1000)
    severity_level = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    suggestion = models.TextField(max_length=None, default='')
    result = models.CharField(max_length=50, default='')
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)