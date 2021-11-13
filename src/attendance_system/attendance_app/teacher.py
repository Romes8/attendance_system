from attendance_app.models import Attendance, Courses, Students, TeacherCourse, Blocks, Settings, StudentClass
from datetime import datetime
from django.db import connection


def get_courses(id):
    try:
        data = []
        query_results = TeacherCourse.objects.filter(teacher=id)
        for query in query_results:
            rooms = Blocks.objects.get(teacher_course=query.id, date = '2021-10-12 8:30:00').room
            room = rooms.campus.name +  ' ' + rooms.building + ' ' + str(rooms.room)
            data.append({
                    "id": query.id,
                    "class_id": query.course_class.class_field.id,
                    "class_name": query.course_class.class_field.name,
                    "subject": query.course_class.course.subject,
                    "room": room})
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

def activate_block(id, dateTime, code):
    try:
        block = Blocks.objects.get(teacher_course=id, date__contains=datetime.date(dateTime.year, dateTime.month, dateTime.day), date__hour=dateTime.hour)
        block.code = code
        block.is_active = True
        block.save(update_fields=["is_active","code"])
        return block.id
    except:
        Exception

def deactivate_block(id, dateTime):
    try:
        block = Blocks.objects.get(teacher_course=id, date_contains=datetime.date(dateTime.year, dateTime.month, dateTime.day), date__hour=datetime.hour)
        block.is_active = False
        block.save(update_fields=["is_active"])
    except:
        Exception
        
def get_students(class_id, teacher_course):
    try:
        students = []
        subject = TeacherCourse.objects.get(id=teacher_course).course_class.course.subject
        query = StudentClass.objects.filter(class_field=class_id)
        for result in query:
            students.append({
                "name": result.student.firstname + ' ' + result.student.lastname,
                "id": result.student.id})
            
        return students, subject
    except:
        Exception

def get_student_attendance(teacher_course, student_id):
    try:
        attendance = []
        student = Students.objects.get(id=student_id)
        course = TeacherCourse.objects.get(id=teacher_course).course_class.course.subject
        name = student.firstname + ' ' + student.lastname
        blocks = Blocks.objects.filter(teacher_course=teacher_course)
        for block in blocks:
            record = Attendance.objects.get(student=student_id, block=block)
            attendance.append({
                "date": block.date,
                "status": record.status
            })
    
        return attendance, name, course
    except:
        return attendance, name, course

def saveChanges(id, isBlocks, period, reminder):
    try:
        settings = Settings.objects.get(teacher=id)
        settings.isblocks = True if isBlocks == 'on' else False
        settings.checkinperiod = period
        settings.reminder = True if reminder == 'on' else False
        settings.save(update_fields=['isblocks', 'checkinperiod', 'reminder'])
    except:
        print(Exception)