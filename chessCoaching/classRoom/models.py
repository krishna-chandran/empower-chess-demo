from django.db import models
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
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
    role_name = models.CharField(max_length=255, unique=True)

class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()

class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)

class UserPageActivity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    percentage_completed = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.page.title}"

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
    feature_name = models.CharField(max_length=255, unique=True)

class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    
    
    class Meta:
        unique_together = ['role', 'feature']
        
class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=255, unique=True)
    package_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity = models.IntegerField()

# class Subscription(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     subscription_start_date = models.DateField()
#     subscription_end_date = models.DateField()
#     payment_details = models.TextField()

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    payment_date = models.DateField()
    expiry_date = models.DateField()
    
class PackageOptions(models.Model):
    option_id = models.AutoField(primary_key=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)