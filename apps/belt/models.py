from __future__ import unicode_literals
import re 
from django.db import models
import bcrypt
from time import gmtime, strftime
# regex for name and email

class Manager(models.Manager):
    def reg_validation(self,postData):
        errors = {}
        # checking length
        if len(postData['name']) < 3 or len(postData['username']) < 3  or len(postData['password']) < 8:
            errors['short'] = "Fields cannot be empty, Name/Username must be more than 3 characters, and password must be at least 8."
        return errors

    def travel_validation(self, postData):
        errors = {}
        # checking length then date validations
        currentDate = strftime("%Y-%m-%d")
        if len(postData['destination']) < 1 or len(postData['description']) < 1 or len(postData['date_start']) < 1 or len(postData['date_end']) < 1:
            errors['empty'] = "Fields cannot be empty."
        if postData['date_start'] <= currentDate:
            errors['past'] = "Start date must be in the future."
        if postData['date_end'] < postData['date_start']:
            errors['past_end'] = "End date must be after start date."
        return errors
    
class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()

class Travels(models.Model):
    user_travels = models.ManyToManyField(Users, related_name="plans")
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = Manager()