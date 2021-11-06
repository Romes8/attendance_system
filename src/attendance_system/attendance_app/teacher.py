from attendance_app.models import TeacherCourse, Blocks, Settings
from datetime import datetime

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