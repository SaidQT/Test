from django.db import models
import re
from datetime import datetime

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name description should be at least 2 characters"
        if len(postData['email'])<0:
            errors['email']='Email is required'
        if len(postData['password'])<8:
            errors['password']="Password must be longer than 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address!"
        elif User.objects.filter(email=postData['email']).exists():
            errors['email']= "Email already in use"
        if postData['password'] != postData['confirm_password']:
            errors['password']="Passwords don't match"
        return errors
class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['dest']) < 2:
            errors["dest"] = "Destination must be at least two character"
        if len(postData['itin']) > 50:
            errors['itin']="Itinerary can be at max 50 characters"
        if postData['date'] and datetime.strptime(postData['date'], '%Y-%m-%d') < datetime.now():
            errors['date'] = "Start date cannot be in the past"
        if postData["date"] and postData['dateend'] and datetime.strptime(postData['dateend'], '%Y-%m-%d') < datetime.strptime(postData["date"], '%Y-%m-%d'):
            errors['enddate'] = "End date should be after start date"
        return errors
    
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=23)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    
class Trip(models.Model):
    country=models.CharField(max_length=45)
    startdate=models.DateField()
    enddate=models.DateField()
    organizer=models.ForeignKey(User,related_name="trips", on_delete=models.CASCADE)
    itinerary=models.TextField()
    travelers=models.ManyToManyField(User,related_name="trip",blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TripManager()
    
