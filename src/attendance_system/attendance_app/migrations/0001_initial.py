# Generated by Django 3.2.8 on 2021-11-12 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'attendance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Blocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('is_active', models.IntegerField()),
                ('code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'blocks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Campuses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'campuses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClassCourses',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'class_courses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'courses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('password', models.CharField(max_length=40)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.IntegerField()),
            ],
            options={
                'db_table': 'login',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'roles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=1)),
                ('room', models.IntegerField()),
            ],
            options={
                'db_table': 'rooms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(db_column='lastName', max_length=50)),
                ('firstname', models.CharField(db_column='firstName', max_length=50)),
                ('phonenumber', models.CharField(blank=True, db_column='phoneNumber', max_length=10, null=True)),
            ],
            options={
                'db_table': 'students',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeacherCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'teacher_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(db_column='lastName', max_length=50)),
                ('firstname', models.CharField(db_column='firstName', max_length=50)),
                ('phonenumber', models.CharField(db_column='phoneNumber', max_length=10)),
            ],
            options={
                'db_table': 'teachers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='attendance_app.teachers')),
                ('isblocks', models.IntegerField(db_column='isBlocks')),
                ('checkinperiod', models.IntegerField(db_column='checkInPeriod')),
                ('reminder', models.IntegerField()),
            ],
            options={
                'db_table': 'settings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='attendance_app.students')),
            ],
            options={
                'db_table': 'student_class',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('is_active', models.IntegerField()),
                ('role', models.ForeignKey(blank=True, db_column='role', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendance_app.roles')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
