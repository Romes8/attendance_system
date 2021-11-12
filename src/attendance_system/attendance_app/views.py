from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import attendance_app.database as database
import attendance_app.student as student
import attendance_app.teacher as teacher
from attendance_app.models import DjangoSession, Login, MyUser, Roles
from datetime import datetime, timedelta
import json
import threading
import subprocess

    
def login_page(request):
        
    if request.method == 'GET':
        print("Get method activated")

    if request.method == 'POST':
        print("POST on index")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user=user)
            request.session.set_expiry(300)
            request.session['username'] = username
            request.session['role'] = user.role.name
            request.session['id'], request.session['name'] = database.get_userID_name(user.role.name, username)
            print("yes")
            return redirect ('/index/')
        else:
            messages.error(request,'username or password not correct')
            return redirect('login')
    
    return render(request, "login.html") 

def logout_page(request):
    try:
        logout(request)
    except KeyError:
        pass
    return redirect("/login/", {})

@login_required
def home_page(request):

    return render(request, "layout_base.html")

@login_required
def index_page(request):
    student.get_courses(request.session.get('id'))
    if request.session.get('role') == 'teacher':
        data = teacher.get_courses(request.session.get('id'))
    else:
        data = student.get_courses(request.session.get('id'))
    return render(request, "index.html", {'data': data})

@login_required
def history_page(request):

    if request.session.get('role') == 'student':
        data = student.history(request.session.get('id'), 'date')
        return render(request, "history.html", {"data": data})
    else:
        return redirect('/index/')


@login_required
def settings_page(request):
    if request.session.get('role') == 'teacher':
        data = teacher.settings(request.session.get('id'))
        return render(request, "settings.html", {'data': data})
    else:
        return redirect('/index/')


@login_required
def active_class(request, teacher_course):

    if request.session.get('role') == 'teacher':
        global start_time
        curDate = datetime.now()
        code = random_string()
        block_id = teacher.activate_block(teacher_course, curDate, code)
        teacher.create_event_block(block_id, request.session.get('id'))
        threading.Timer(900, teacher.deactivate_block, [teacher_course, curDate]).start()
        return render(request, "active_page.html", {'code':code})
    return redirect('/index/')


@login_required
def class_selected(request, class_course):
    type = None
    active_blocks = student.check_active(class_course, datetime.now())
    if len(active_blocks) == 1:
        type = "block"
    elif len(active_blocks) > 1:
        type = "lesson"
    return render(request, "class.html", {"active_blocks": active_blocks, "type": type})


@login_required          
def details_page(request, teacher_course, class_id):
    print("Details page")
    students = teacher.get_students(class_id)
    data = teacher.get_courses(request.session.get('id'))
    for dat in data:
        if dat['class_id'] == class_id:
            subject_name = dat['subject']
            
    return render(request, "details.html", {"students": students, "teacher_course":teacher_course, "subject_name":subject_name})

@login_required
def student_details(request):
    json_data = json.loads(request.POST.get('json_data'))
    student_id = json_data['student_id']
    teacher_course = json_data['teacher_course']
    course = json_data['course']
    data = teacher.get_student(teacher_course, student_id)
    return render(request, "student.html", {"course":course, "data":data})

@login_required
def extend_session(request):
    print(request.POST)
    return True


@csrf_exempt
def check_code(request):
    data = json.loads(request.POST.get('json_data'))
    print(data)
    code = data['code']
    blocks = data['blocks']
    student_id = data['student_id']
    if student.check_entered_code(blocks,code):
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


# check for the right wifi connection 

if "Vartic2" in subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8'):
    print('good network')

    
def page_404(request, *args, **argv):
    response = render(request,'404.html', {})
    response.status_code = 404
    return response


def page_500(request):
    return render(request,'500.html', {})