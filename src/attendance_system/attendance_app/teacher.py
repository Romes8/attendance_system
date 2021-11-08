from attendance_app.models import TeacherCourse, Blocks, Settings, StudentClass
from datetime import datetime
from django.db import connection

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


def create_event_block(block_id, teacher_id):
    try:
        start_time = Blocks.objects.get(id=1).date
        print(start_time)
        timer = int(Settings.objects.get(teacher=teacher_id).checkInPeriod)
        print(timer)
        cur = connecton.cursor()
        cur.execute = ("CREATE EVENT deactivate_block1 ON SCHEDULE AT '2021-11-08 15:40:00' + INTERVAL 15 MINUTE ON COMPLETION PRESERVE DO UPDATE blocks SET is_active = 0 WHERE id = 1;")
        cur.close()
        return 0
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
        block = Blocks.objects.get(teacher_course=id, date__contains=datetime.date(2021, 10, 12), date__hour=8)
        print(blocks)
        block.code = code
        block.is_active = True
        block.save(update_fields=["is_active","code"])
        return block.id
    except:
        Exception

def deactivate_block(id, dateTime):
    try:
        block = Blocks.objects.get(teacher_course=id, date=datetime.date(dateTime))
        block.is_active = False
        block.save(update_fields=["is_active"])
    except:
        Exception
        
def get_students(class_id):
    print(class_id)
    try:
        students = []
        query = StudentClass.objects.filter(class_field=class_id)
        for result in query:
            students.append({
                "firstname": result.student.firstname,
                "lastname": result.student.lastname,
                "id": result.student.id})
            
        return students
    except:
        Exception
        print("exeption")