# Generated by Django 4.1.3 on 2022-11-10 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('assignment', models.FileField(upload_to='')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('submission_limit', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_code', models.CharField(max_length=8)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department')),
                ('lecturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.lecturer')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_id', models.CharField(max_length=20)),
                ('semester_name', models.CharField(choices=[('first', 'first'), ('second', 'second')], max_length=10)),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('grade', models.FloatField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField()),
                ('date_graded', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.assignment')),
                ('student_submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='submissions.studentsubmission')),
            ],
        ),
        migrations.CreateModel(
            name='CourseReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submissions.semester'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='lecturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.lecturer'),
        ),
    ]