from django.db import models

# Create your models here.
class User_Info(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 200)
    email = models.EmailField()
    dob = models.DateField()