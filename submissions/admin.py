from django.contrib import admin
from .models import Semester, Course, CourseReg, Assignment, StudentSubmission, Result


admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(CourseReg)
admin.site.register(Assignment)
admin.site.register(StudentSubmission)
admin.site.register(Result)

# Register your models here.
