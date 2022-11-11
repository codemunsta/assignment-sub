from django.shortcuts import render, redirect
from .models import Semester, Course, CourseReg, Assignment, StudentSubmission, Result
from users.models import Faculty, Department, Lecturer, Student
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def create_semester(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                data = request.POST
                semester = Semester.objects.create(
                    semester_name=data['semester_name'],
                    date_from=data['date_from'],
                    date_to=data['date_to'],
                )
                semester.save()
                return redirect('home')
            else:
                return render(request, 'create_semester.html')
        else:
            return redirect('home')
    else:
        return redirect('login')


def create_course(request):
    if request.user.is_authenticated:
        try:
            lecturer = Lecturer.objects.get(staff=request.user)
        except ObjectDoesNotExist:
            messages.info('Unauthorized request')
            return redirect('home')
        if request.method == 'POST':
            data = request.POST
            department = lecturer.department
            print(data['semester'])
            semester = Semester.objects.get(id=data['semester'])
            course = Course.objects.create(
                course_name=data['course_name'],
                course_code=data['course_code'],
                semester=semester,
                department=department,
                lecturer=lecturer,
            )
            course.save()
            return redirect('lecturer_dashboard', pk=request.user.id)
        else:
            semesters = Semester.objects.all()
            context = {
                'semesters': semesters
            }
            return render(request, 'create_course.html', context=context)
    else:
        return redirect('login')


def courses(request, faculty_id):
    faculty = Faculty.objects.get(id=faculty_id)
    departments = Department.objects.filter(faculty=faculty)
    faculty_courses = []
    for department in departments:
        department_courses = Course.objects.filter(department=department)
        for course in department_courses:
            faculty_courses.append(course)
    context = {
        'courses': faculty_courses
    }
    return render(request, 'courses.html', context=context)


def register_course(request, course_code):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
        except ObjectDoesNotExist:
            messages.info('login to register course')
            return redirect('login')
        course = Course.objects.get(course_code=course_code)
        course_reg = CourseReg.objects.create(
            course=course,
            student=student,
        )
        course_reg.save()
        return redirect('courses', faculty_id=student.faculty.id)
    else:
        return redirect('login')


def create_assignment(request):
    if request.user.is_authenticated:
        try:
            lecturer = Lecturer.objects.get(staff=request.user)
        except ObjectDoesNotExist:
            messages.info('Unauthorized request')
            return redirect('home')
        if request.method == 'POST':
            data = request.POST
            files = request.FILES
            course = Course.objects.get(id=data['course'])
            ass = Assignment.objects.create(
                name=data['name'],
                assignment=files['assignment'],
                lecturer=lecturer,
                submission_limit=data['submission_limit'],
                course=course
            )
            ass.save()
            return redirect('lecturer_dashboard', pk=request.user.id)
        else:
            all_courses = Course.objects.filter(lecturer=lecturer)
            context = {
                'courses': all_courses
            }
            return render(request, 'create_assignment.html', context=context)
    else:
        return redirect('login')


def submit_assignment(request, ass_id):
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
        except ObjectDoesNotExist:
            messages.info('login as a student')
            return redirect('login')
        if request.method == 'POST':
            files = request.FILES
            assignment_t = Assignment.objects.get(id=ass_id)
            submission = StudentSubmission.objects.create(
                student=student,
                assignment=assignment_t,
                file=files['Assignment'],
            )
            submission.save()
            return redirect('student_dashboard', pk=request.user.id)
        else:
            assignment_t = Assignment.objects.get(id=ass_id)
            context = {
                'ass': assignment_t,
            }
            return render(request, 'submit_assignment.html', context=context)
    else:
        return redirect('login')


def course_assignments(request, ass_id):
    if request.user.is_authenticated:
        try:
            lecturer = Lecturer.objects.get(staff=request.user)
        except ObjectDoesNotExist:
            messages.info('Unauthorized request')
            return redirect('home')
        ass = Assignment.objects.get(id=ass_id, lecturer=lecturer)
        student_submissions = StudentSubmission.objects.filter(assignment=ass)
        context = {
            'assignment': ass,
            'student_submissions': student_submissions
        }
        return render(request, 'course_assignments.html', context=context)
    else:
        return redirect('login')


def grade_assignment(request, stud_ass_id):
    if request.user.is_authenticated:
        try:
            lecturer = Lecturer.objects.get(staff=request.user)
        except ObjectDoesNotExist:
            messages.info('Unauthorized request')
            return redirect('home')
        if request.method == 'POST':
            ass = StudentSubmission.objects.get(id=stud_ass_id)
            grade = request.POST['grade']
            ass.grade = grade
            ass.save()
            result = Result.objects.create(
                assignment=ass.assignment,
                student_submission=ass,
                grade=grade,
            )
            result.save()
            return redirect('lecturer_dashboard', pk=request.user.id)
        else:
            ass = StudentSubmission.objects.get(id=stud_ass_id)
            context = {
                'assignment': ass,
                'stud_ass_id': stud_ass_id,
            }
            return render(request, 'grade_assignment.html', context=context)
    else:
        return redirect('login')


def lecturer_dashboard(request, pk):
    if request.user.is_authenticated:
        if request.user.id != pk:
            messages.info('unauthorized')
            return redirect('home')
        try:
            lecturer = Lecturer.objects.get(staff=request.user)
        except ObjectDoesNotExist:
            messages.info('Unauthorized request')
            return redirect('home')
        department = lecturer.department
        faculty = department.faculty
        lecturer_courses = Course.objects.filter(lecturer=lecturer)
        all_courses = []
        for course in lecturer_courses:
            assignments = Assignment.objects.filter(course=course, lecturer=lecturer)
            subject = {
                'course': course,
                'assignments': assignments,
            }
            all_courses.append(subject)
        context = {
            'lecturer': lecturer,
            'faculty': faculty,
            'department': department,
            'courses': all_courses,
        }
        return render(request, 'lecturer_dashboard.html', context=context)
    else:
        return redirect('login')


def result_page(request, ass_id):
    if request.user.is_authenticated:
        try:
            lecturer = Lecturer.objects.get(staff=request.user)
        except ObjectDoesNotExist:
            messages.info('Unauthorized request')
            return redirect('home')
        ass = Assignment.objects.get(id=ass_id, lecturer=lecturer)
        results = Result.objects.filter(assignment=ass)
        context = {
            'results': results,
        }
        return render(request, 'result_page.html', context=context)
    else:
        return redirect('login')


def student_dashboard(request, pk):
    if request.user.is_authenticated:
        if request.user.id != pk:
            messages.info('unauthorized')
            return redirect('home')
        try:
            student = Student.objects.get(user=request.user)
        except ObjectDoesNotExist:
            messages.info('login as a student')
            return redirect('login')
        faculty = student.faculty
        department = student.department
        courses_registered = CourseReg.objects.filter(student=student)
        results = StudentSubmission.objects.filter(student=student)
        assignments = []
        for courses_reg in courses_registered:
            course = courses_reg.course
            ass = Assignment.objects.filter(course=course)
            item = {
                'course': course,
                'assignments': ass,
            }
            assignments.append(item)
        context = {
            'student': student,
            'faculty': faculty,
            'department': department,
            'courses_registered': courses_registered,
            'results': results,
            'assignments': assignments
        }
        return render(request, 'student_dashboard.html', context=context)

    else:
        return redirect('login')


# Create your views here.
