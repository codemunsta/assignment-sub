from django.urls import path
from . import views


urlpatterns = [
    path('super_admin/create/semester', views.create_semester, name='create_semester'),
    path('lecturer/create/course', views.create_course, name='create_course'),
    path('student/courses/<int:faculty_id>/register', views.courses, name='courses'),
    path('student/register/<str:course_code>', views.register_course, name='register_course'),
    path('student/unregister/<int:pk>', views.unregister_course, name='unregister_course'),
    path('lecturer/create/assignment', views.create_assignment, name='create_assignment'),
    path('student/submit/<int:ass_id>', views.submit_assignment, name='submit_assignment'),
    path('lecturer/assignments/<int:ass_id>/submissions', views.course_assignments, name='course_assignments'),
    path('lecturer/grade/<int:stud_ass_id>', views.grade_assignment, name='grade_assignment'),
    path('dashboard/lecturer/<int:pk>', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('results/<int:ass_id>', views.result_page, name='result_page'),
    path('dashboard/student/<int:pk>', views.student_dashboard, name='student_dashboard'),
    path('student/view/assignments', views.view_assignment, name='view_assignment'),
    path('lecturer/view/assignments', views.lecturer_assignment, name='lecturer_assignments'),
    path('lecturer/grade/submission/<int:pk>', views.grade_assignment, name='grade_result'),
    path('student/view/all_results', views.student_view_result, name='student_result'),
    path('lecturer/view/results', views.lecturer_view_results, name='lecture_view_results'),
    path('lecturer/view/assignment/results/<int:pk>', views.view_assignment_result, name='view_result')
]
