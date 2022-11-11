import os
import binascii
from django.db import models
from django.contrib.auth.models import User


class Faculty(models.Model):
    institution_name = models.CharField(max_length=30)
    faculty_name = models.CharField(max_length=30)
    shorts = models.SlugField(max_length=3)

    def __str__(self):
        return self.faculty_name


class Department(models.Model):
    department_name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    shorts = models.SlugField(max_length=3)

    def __str__(self):
        return self.department_name


class Lecturer(models.Model):

    Type = (
        ('Senior_Professor', 'Senior_Professor'),
        ('Professor', 'Professor'),
        ('Lecturer_1', 'Lecturer_1'),
        ('Lecturer_2', 'Lecturer_2'),
        ('Lecturer_3', 'Lecturer_3'),
        ('Junior_Lecturer', 'Junior_Lecturer'),
        ('Graduate_assistant', 'Graduate_assistant')
    )
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    staff_name = models.CharField(max_length=100)
    staff_type = models.CharField(max_length=20, choices=Type)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    staff_app_num = models.CharField(max_length=15)
    status = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.staff_name}'


class Student(models.Model):

    Sex = (
        ('male', 'male'),
        ('female', 'female'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    title = models.CharField(max_length=10)
    mat_number = models.CharField(max_length=20)
    admission_id = models.CharField(max_length=15)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    nationality = models.CharField(max_length=40)
    sex = models.CharField(max_length=10, choices=Sex)
    dob = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstname} {self.lastname} | {self.mat_number}'

# Create your models here.
