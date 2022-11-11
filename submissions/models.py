import os
import binascii
from django.db import models
from users.models import Department, Lecturer, Student


class Semester(models.Model):

    Name = (
        ('first', 'first'),
        ('second', 'second'),
    )
    semester_id = models.CharField(max_length=20)
    semester_name = models.CharField(max_length=10, choices=Name)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    def __str__(self):
        return f'{self.semester_name} {self.date_from}'

    def save(self, *args, **kwargs):
        if not self.semester_id:
            self.semester_id = f'{self.generate_encrypt()}'
            return super().save(*args, **kwargs)

    @classmethod
    def generate_encrypt(cls):
        return binascii.hexlify(os.urandom(10)).decode()


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=8)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.course_code}'


class CourseReg(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.course_code} | {self.student.mat_number}'


class Assignment(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.FileField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    submission_limit = models.DateTimeField()

    def __str__(self):
        return f'{self.name}'


class StudentSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField()
    grade = models.FloatField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.mat_number} | {self.assignment.name}'


class Result(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_submission = models.OneToOneField(StudentSubmission, on_delete=models.CASCADE)
    grade = models.FloatField()
    date_graded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student_submission.student.mat_number} | {self.assignment.name}'

# Create your models here.
