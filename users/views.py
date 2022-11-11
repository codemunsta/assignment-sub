from django.shortcuts import render, redirect
from .models import Faculty, Department, Lecturer, Student
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def create_faculty(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            if request.method == 'POST':
                data = request.POST
                institution_name = data['institution_name']
                faculty_name = data['faculty_name']
                shorts = data['shorts']
                faculty = Faculty.objects.create(
                    institution_name=institution_name,
                    faculty_name=faculty_name,
                    shorts=shorts,
                )
                faculty.save()
                return redirect('home')
            else:
                return render(request, 'create_faculty.html')
        else:
            return redirect('register')
    else:
        return redirect('register')


def create_department(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            if request.method == 'POST':
                data = request.POST
                faculty = Faculty.objects.get(id=data['faculty'])
                department = Department.objects.create(
                    department_name=data['department_name'],
                    shorts=data['shorts'],
                    faculty=faculty
                )
                department.save()
                return redirect('home')
            else:
                faculties = Faculty.objects.all()
                context = {
                    'faculties': faculties
                }
                return render(request, 'create_department.html', context=context)
        else:
            return redirect('register')
    else:
        return redirect('register')


def register_lecturer(request):
    if request.method == 'POST':
        data = request.POST
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            department = Department.objects.get(id=data['department'])
            lecturer = Lecturer.objects.create(
                staff=user,
                staff_name=f'{firstname} {lastname}',
                staff_type=data['staff_type'],
                department=department,
                status=True,
            )
            lecturer.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('lecturer_dashboard', pk=request.user.id)
        else:
            messages.info('password mismatch')
            return redirect('register_lecturer')
    else:
        departments = Department.objects.all()
        context = {
            'departments': departments
        }
        return render(request, 'register_lecturer.html', context=context)


def register_student(request):
    if request.method == 'POST':
        data = request.POST
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            faculty = Faculty.objects.get(id=data['faculty'])
            department = Department.objects.get(id=data['department'])
            student = Student.objects.create(
                user=user,
                firstname=firstname,
                lastname=lastname,
                middle_name=data['middle_name'],
                title=data['title'],
                mat_number=data['mat_number'],
                admission_id=data['admission_id'],
                department=department,
                nationality=data['nationality'],
                sex=data['sex'],
                dob=data['dob'],
                faculty=faculty,
            )
            student.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('student_dashboard', pk=request.user.id)
        else:
            messages.info('password mismatch')
            return redirect('register_student')
    else:
        faculties = Faculty.objects.all()
        departments = Department.objects.all()
        context = {
            'faculties': faculties,
            'departments': departments,
        }
        return render(request, 'register_student.html', context=context)


def user_login(request):
    if request.user.is_authenticated:
        try:
            Student.objects.get(user=request.user)
            return redirect('student_dashboard', pk=request.user.id)
        except ObjectDoesNotExist:
            try:
                Lecturer.objects.get(staff=request.user)
                return redirect('lecturer_dashboard', pk=request.user.id)
            except ObjectDoesNotExist:
                return redirect('home')
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                Student.objects.get(user=request.user)
                return redirect('student_dashboard', pk=request.user.id)
            except ObjectDoesNotExist:
                try:
                    Lecturer.objects.get(staff=request.user)
                    return redirect('lecturer_dashboard', pk=request.user.id)
                except ObjectDoesNotExist:
                    return redirect('home')
        else:
            messages.info(request, 'invalid password')
            return redirect('login')
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    if request.user.is_authenticated:
        try:
            Student.objects.get(user=request.user)
            return redirect('student_dashboard', pk=request.user.id)
        except ObjectDoesNotExist:
            try:
                Lecturer.objects.get(staff=request.user)
                return redirect('lecturer_dashboard', pk=request.user.id)
            except ObjectDoesNotExist:
                return redirect('home')
    else:
        return redirect('login')


# Create your views here.
