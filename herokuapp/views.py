from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import herokuapp.database as database
import herokuapp.student as student
import herokuapp.teacher as teacher
from datetime import datetime, timedelta
import json
import threading
from django.conf import settings


# Authenticate and login the user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user=user)
            request.session.set_expiry(300)
            request.session['username'] = username
            request.session['role'] = user.role.name
            request.session['id'], request.session['name'] = database.get_userID_name(user.role.name, username)
            return redirect('/index/')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')

    return render(request, "login.html")


# Logs out the user, ending the session
def logout_page(request):
    try:
        logout(request)
    except KeyError:
        pass
    return redirect("/login/", {})


#
@login_required
def home_page(request):
    return render(request, "layout_base.html")


# Index page:
# students - courses they attend
# tecahers - classes + courses they teach
@login_required
def index_page(request):
    if request.session.get('role') == 'teacher':
        data = teacher.get_courses(request.session.get('id'))
    else:
        data = student.get_courses(request.session.get('id'))
    return render(request, "index.html", {'data': data})


# Attendance history of the student
@login_required
def history_page(request):
    if request.session.get('role') == 'student':
        data = student.history(request.session.get('id'), 'date')
        return render(request, "history.html", {"data": data})
    else:
        return redirect('/index/')


# Settings page for teachers
@login_required
def settings_page(request):
    if request.session.get('role') == 'teacher':
        if request.method == 'POST':
            isBlocks = request.POST.get('isBlocks')
            period = request.POST.get('period')
            reminder = request.POST.get('reminder')
            teacher.saveChanges(request.session.get('id'), isBlocks, period, reminder)
        data = teacher.settings(request.session.get('id'))
        return render(request, "settings.html", {'data': data})
    else:
        return redirect('/index/')


# Page that displays the code and activates the block
@login_required
def active_class(request, teacher_course):
    if request.session.get('role') == 'teacher':
        curDate = datetime.now()
        print(curDate)
        print("trynng 1")
        code = random_string()
        settings = teacher.settings(request.session.get('id'))
        if settings['isBlocks']:
            teacher.activate_block(teacher_course, curDate, code)
            threading.Timer(settings["period"], teacher.deactivate_block, [teacher_course, curDate]).start()
        else:
            teacher.activate_lesson(teacher_course, curDate, code)
            threading.Timer(settings["period"], teacher.deactivate_lesson, [teacher_course, curDate]).start()
        return render(request, "active_page.html", {'code': code})
    return redirect('/index/')


# Checks if the block is active and redirects to the page to enter the code
@login_required
def class_selected(request, class_course):
    type = None
    active_blocks = student.check_active(class_course, datetime.now())
    if request.META['HTTP_X_FORWARDED_FOR'] in settings.ALLOWED_IP_BLOCKS:
        if len(active_blocks) == 1:
            type = "block"
        elif len(active_blocks) > 1:
            type = "lesson"
        allow = True
    else:
        allow = False
    return render(request, "class.html", {"active_blocks": active_blocks, "type": type, "allow": allow})


#
@login_required
def details_page(request, teacher_course, class_id):
    students, subject_name = teacher.get_students(class_id, teacher_course)
    return render(request, "details.html",
                  {"students": students, "teacher_course": teacher_course, "subject_name": subject_name})


@login_required
def student_details(request, teacher_course, student_id):
    data, name, course = teacher.get_student_attendance(teacher_course, student_id)
    return render(request, "student.html", {"data": data, "name": name, "course": course})


def forgot_pass(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = database.forgot_pass(email)
        return render(request, "forgotpass.html", {"message": message})
    return render(request, "forgotpass.html")


def change_pass(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        message = database.change_pass(1, password)
        return render(request, "changepass.html", {"message": message})
    return render(request, "changepass.html")


@csrf_exempt
def check_code(request):
    data = json.loads(request.POST.get('json_data'))
    code = data['code']
    blocks = data['blocks']
    student_id = data['student_id']
    if student.check_entered_code(blocks, code):
        if student.check_as_present(student_id, blocks):
            return HttpResponse("Valid code! You are registered as present.")
        else:
            return HttpResponse("You already checked in as present.")
    return HttpResponse("Invalid code! Please try again.")


import random
import string


def random_string():
    str = ''.join((random.choice(string.ascii_uppercase) for x in range(4)))
    str += ''.join((random.choice(string.digits) for x in range(2)))
    lst = list(str)
    random.shuffle(lst)
    finalStr = ''.join(lst)
    return finalStr



def page_404(request, *args, **argv):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def page_500(request):
    return render(request, '500.html', {})