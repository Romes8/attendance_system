from django.db import models

class Login(models.Model):
    username = models.CharField(unique=True, max_length=20, blank=True, null=True)
    password = models.CharField(max_length=40)
    role = models.ForeignKey('Roles', models.DO_NOTHING, db_column='role', blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'login'
        
class Roles(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'

class Rooms(models.Model):
    campus = models.ForeignKey('Campuses', models.DO_NOTHING, blank=True, null=True)
    building = models.CharField(max_length=1)
    room = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rooms'

class Campuses(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campuses'

class Students(models.Model):
    lastname = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('Login', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'

class Teachers(models.Model):
    lastname = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=10)  # Field name made lowercase.
    user = models.ForeignKey('Login', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teachers'

class TeacherCourse(models.Model):
    teacher = models.ForeignKey('Teachers', models.DO_NOTHING, blank=True, null=True)
    course_class = models.ForeignKey('ClassCourses', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher_course'

class ClassCourses(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey('Courses', models.DO_NOTHING, blank=True, null=True)
    class_field = models.ForeignKey('Classes', models.DO_NOTHING, db_column='class_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'class_courses'


class Classes(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classes'

class Courses(models.Model):
    subject = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'courses'

class Attendance(models.Model):
    student = models.ForeignKey('Students', models.DO_NOTHING)
    block = models.ForeignKey('Blocks', models.DO_NOTHING)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'attendance'

class Blocks(models.Model):
    teacher_course = models.ForeignKey('TeacherCourse', models.DO_NOTHING)
    room = models.ForeignKey('Rooms', models.DO_NOTHING)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blocks'

class Settings(models.Model):
    teacher = models.OneToOneField('Teachers', models.DO_NOTHING, primary_key=True)
    isblocks = models.IntegerField(db_column='isBlocks')  # Field name made lowercase.
    checkinperiod = models.IntegerField(db_column='checkInPeriod')  # Field name made lowercase.
    reminder = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'settings'
