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
        

def get_courses(id):
    try:
        data = []
        query_results = TeacherCourse.objects.filter(teacher=id)
        for query in query_results:
            print(query.id)
            rooms = Blocks.objects.get(teacher_course=query.id, date = '2021-10-12 8:30:00').room
            room = rooms.campus.name +  ' ' + rooms.building + ' ' + str(rooms.room)
            data.append({
                    "id": query.id,
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
        query = Settings.objects.get(teacher=id)
        data = {
            'isBlocks': query.isblocks,
            'period': query.checkinperiod,
            'reminder': query.reminder}
        return data
    except:
        Exception

def activate_lesson(id, date, code):
    try:
        blocks = Blocks.objects.filter(teacher_course=id, date__contains=datetime.date(date.year, date.month, date.day))
        for block in blocks:
            block.code = code
            block.is_active = True
            block.save(update_fields=["is_active", "code"])
    except:
        Exception

def deactivate_lesson():
    try:
        lesson = Blocks.objects.filter(teacher_course=3, date__contains=datetime.date(2021, 10, 12))
        for block in lesson:
            block.is_active = False
            block.save(update_fields=["is_active"])
            
    except:
        Exception

def activate_block(id, date, code):
    try:
        blocks = Blocks.objects.filter(teacher_course=id, date__contains=datetime.date(2021, 10, 12), date__hour=8)
        print(blocks)
        for block in blocks:
            block.code = code
            block.is_active = True
            block.save(update_fields=["is_active","code"])
    except:
        Exception

def deactivate_block(id, dateTime):
    try:
        blocks = Blocks.objects.get(teacher_course=id, date=datetime.date(dateTime))
        for block in blocks:
            block.is_active = False
            block.save(update_fields=["is_active"])
    except:
        Exception

def check_active(id, date):
    try:
        class_id = StudentClass.objects.get(student=id).class_field.id
        print(class_id)
        class_course_id = ClassCourses.objects.filter(class_field=1)
        print(class_course_id)
        teacher_course_id = TeacherCourse.objects.get(course_class=class_course_id).id
        print(teacher_course_id)
        block = Blocks.objects.get(teacher_course=teacher_course_id, date__contains=datetime.date(2021, 10, 12))
        print(block)
        if block.is_active:
            print("true")
            return block.id
    except:
        Exception

def check_entered_code(block_id,code):
    try:
        valid_code = Blocks.objects.get(id=block_id).code
        if code == valid_code:
            return True
        return False
    except:
        Exception