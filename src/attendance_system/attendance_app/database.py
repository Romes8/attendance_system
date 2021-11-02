from attendance_app.models import Settings, Blocks, Login, Students, TeacherCourse, Teachers, ClassCourses, Classes, Courses, Attendance
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
            print("hey")
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
        

def get_courses(id):
    try:
        data = []
        query_results = TeacherCourse.objects.filter(teacher=id)
        for query in query_results:
            print(query.id)
            rooms = Blocks.objects.get(teacher_course=query.id, date = '2021-10-12 8:30:00').room
            room = rooms.campus.name +  ' ' + rooms.building + ' ' + str(rooms.room)
            data.append({
                    "class": query.course_class.class_field.name,
                    "subject": query.course_class.course.subject,
                    "room": room})
        return data

    except:
        Exception

def history(id, sort):
    try:
        data = []
        order = "-block__date"
        if sort == 'subject':
            order = "block__teacher_course__course_class__course__subject"
        query_results = Attendance.objects.select_related("block").order_by(order).filter(student_id=id)
        for query in query_results:
            data.append({
                'date': query.block.date.strftime("%Y-%m-%d, %H:%M:%S"), 
                'subject': query.block.teacher_course.course_class.course.subject, 
                'status': query.status})
        return data
    except:
        Exception

def settings(id):
    try:
        data = []
        query = Settings.objects.get(teacher=id)
        data.append({
            'isBlocks': query.isBlocks,
            'period': query.checkInPeriod,
            'reminder': query.reminder})
        return data
    except:
        Exception
