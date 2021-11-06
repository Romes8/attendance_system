from attendance_app.models import StudentClass, Settings, Blocks, Login, Students, TeacherCourse, Teachers, ClassCourses, Classes, Courses, Attendance
from hashlib import sha1
import datetime
from django.contrib.auth.backends import BaseBackend




class MyBackend(BaseBackend):
    def authenticate(self, username, password):
        if Login.objects.filter(username=username).exists():
            l = Login.objects.get(username=username)
            if l.password == sha1(sha1(password.encode()).digest()).hexdigest().upper():
                return l
        else:
            return None


def get_role(username, password):
    try:
        l = Login.objects.get(username=username)
        if l.password == sha1(sha1(password.encode()).digest()).hexdigest().upper():
            return l.role.name
        else:
            return None
    except:
        Exception


def get_userID_name(role, username):
    try:
        user_id = Login.objects.get(username=username).id
        if role == 'student':
            user = Students.objects.get(user_id=user_id)
        else :
            user = Teachers.objects.get(user_id=user_id)
        id = user.id
        name = user.lastname + ' ' + user.firstname
        return id, name
    except:
        raise Exception
        
