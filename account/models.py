from django.db import models
from django.contrib.auth.models import User
from administration.models import Designation

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    photo = models.ImageField(upload_to='admin/')
    date_of_birth = models.DateField(null=True, blank=True) 


    gender_select = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(choices=gender_select, max_length=6)
    
    employee_select = (
        ('admin', 'Admin'),
        ('professor', 'Professor'),
        ('teacher', 'Teacher'),
        ('register', 'Register'),
        ('student', 'Student'),
        ('peon','Peon'),
    )
    employee_type = models.CharField(choices=employee_select, max_length=15)

    def __str__(self):
        return self.name
