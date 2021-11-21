from django.http.response import HttpResponse
from herokuapp.models import Attendance, StudentClass, ClassCourses, TeacherCourse, Blocks
import datetime


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

def get_courses(id):
    try:
        data =[]
        class_id = StudentClass.objects.get(student=id).class_field.id
        courses = ClassCourses.objects.filter(class_field=class_id)
        for course in courses:
            data.append({
                "class_course_id": course.id,
                "course_name": course.course.subject
            })
        return data
    except:
        Exception

def check_active(id, date):
    try:
        active_blocks = []
        teacher_course_id = TeacherCourse.objects.get(course_class=id).id
        blocks = Blocks.objects.filter(teacher_course=teacher_course_id, date__contains=datetime.date(date.year, date.month, date.day))
        for block in blocks:
            if block.is_active:
                active_blocks.append(block.id)
        return active_blocks
    except:
        Exception

def check_entered_code(blocks,code):
    try:
        valid_code = Blocks.objects.get(id=blocks[0]).code
        if code == valid_code:
            return True
        return False
    except:
        Exception


def check_as_present(student_id, blocks):
    try:
        for block in blocks:
            if Attendance.objects.filter(student_id=student_id, block_id=block).exists():

                state = False
            else: 
                Attendance.objects.create(student_id=student_id, block_id=block, status="present")
                state = True
        return state
    except:
        Exception
