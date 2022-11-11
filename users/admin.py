from django.contrib import admin
from .models import Faculty, Department, Lecturer, Student


admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Lecturer)
admin.site.register(Student)

# Register your models here.
