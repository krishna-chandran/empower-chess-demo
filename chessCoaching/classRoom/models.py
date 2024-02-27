from django.db import models
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User as AuthUser

# Create your models here.
def no_future(value):
    today = datetime.date.today()
    if value > today:
        raise ValidationError('Date of Birth cannot be in the future.')

class Student(models.Model):
    student_id              = models.AutoField(primary_key=True)
    first_name              = models.CharField(max_length=255)
    last_name               = models.CharField(max_length=255)
    date_of_birth           = models.DateField(validators=[no_future])
    address                 = models.CharField(max_length=900)
    city                    = models.CharField(max_length=255)
    state                   = models.CharField(max_length=255)
    country                 = models.CharField(max_length=255)
    father_name             = models.CharField(max_length=255)
    mother_name             = models.CharField(max_length=255)
    phone                   = models.CharField(max_length=255)
    bloodgrp                = models.CharField(max_length=2,null=True,blank=True)
    student_email           = models.EmailField(max_length=255,unique=True)
    academy                 = [("A","Apple"),("B","Balls")]
    academy_interested      = models.CharField(max_length=255,choices=academy,)
    password                = models.CharField(max_length=255)

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)

class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()
    payment_details = models.TextField()

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    # other course details

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

class UserAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_date = models.DateField()
    grade = models.CharField(max_length=5)
    comments = models.TextField()

class Feature(models.Model):
    id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=255)

class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)