from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import SESSION_KEY, login, logout
import attendance_app.database as database
import attendance_app.student as student
import attendance_app.teacher as teacher
from attendance_app.models import DjangoSession, Login
from datetime import datetime, timedelta
import json
start_time = datetime.now()
sessionDict = {}
user = None
wrongLogin = 'false' #variable for error diplay message while logging in 

import subprocess

    
def login_page(request):
    global wrongLogin
    global sessionDict
    global user
        
    if request.method == 'GET':
        print("Get method activated")

    if request.method == 'POST':
        wrongLogin = 'false'  #set login check back to deafault
        print("POST on index")
        username = request.POST.get('username')
        password = request.POST.get('password')
        backend = database.MyBackend()
        user = backend.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user=user)
            request.session.set_expiry(20)
            request.session['alert'] = True

            if request.session.exists(session_key=request.session.session_key):
                print(request.session.session_key)
            sessionDict['username'] = user.username
            sessionDict['role'] = user.role.name
            sessionDict['id'], sessionDict['name'] = database.get_userID_name(sessionDict['role'], sessionDict['username'])
            print(sessionDict)
            user.is_active=1
            user.save(update_fields=["is_active"])
            return redirect('/index/')
        else:
            wrongLogin = 'true'
            return redirect('/login/')
    # refers to index page and what contect is going to be displayed  when post method is applied
    
    return render(request, "login.html", {'wrongLogin': wrongLogin}) #sending message for wrong login`

def logout_page(request):
    global user
    try:
        logout(request)
        user.is_active=0
        user.save(update_fields=["is_active"])
        sessionDict.clear()
        user=None
    except KeyError:
        pass
    return redirect("/login/", {})

# Create your views here.
def home_page(request):
    if user is not None:
        if user.is_active:
            return render(request, "layout_base.html")
    
    return redirect('/login/')


def index_page(request):
    global wrongLogin
    if user is not None:
        if user.is_active:
            student.get_courses(sessionDict['id'])
            if sessionDict['role'] == 'teacher':
                data = teacher.get_courses(sessionDict['id'])
                return render(request, "index.html", {'sessionDict': sessionDict, 'data': data})
            else:
                data = student.get_courses(sessionDict['id'])
                return render(request, "index.html", {'sessionDict': sessionDict, 'data': data})
    else:
        return redirect('/login/')

def history_page(request):
    if user is not None:
        if user.is_active:
            if sessionDict['role'] == 'student':
                data = student.history(sessionDict['id'], 'date')
                return render(request, "history.html", {"data": data, "sessionDict": sessionDict})
            else:
                redirect('/index/')
    else:
        return redirect('/login/')

def settings_page(request):
    if user is not None:
        if user.is_active:
            if sessionDict['role'] == 'teacher':
                data = teacher.settings(sessionDict['id'])
                print(data)
                print(sessionDict)
                return render(request, "settings.html", {'sessionDict': sessionDict, 'data': data})
            else:
                return redirect('/index/')
    return redirect('/login/')

def active_class(request, teacher_course):
    if user is not None:
        if user.is_active:
            if sessionDict['role'] == 'teacher':
                global start_time
                curDate = datetime.now()
                code = random_string()
                block_id = teacher.activate_block(teacher_course, curDate, code)
                teacher.create_event_block(block_id, sessionDict['id'])
                return render(request, "active_page.html", {'code':code, "sessionDict": sessionDict})
            return redirect('/index/')
    return redirect('/login/')

def active_session(request):
    session_key = request.session.session_key
    if request.session.exists(session_key):
        record = DjangoSession.objects.get(session_key=session_key)
        if record.expire_date < datetime.now():
            if extend_session():
                request.session['alert'] = True
                record.expire_date = datetime.now() + timedelta(minutes=20)
                return True                         #session extended 
            else:
                record.delete()
                return False                        #session disconnected
        return True                                 #session still active             
    else:
        return False                                #session disconnected

def class_selected(request, class_course):
    if user is not None:
        if user.is_active: 
            type = None
            active_blocks = student.check_active(class_course, datetime.now())
            if len(active_blocks) == 1:
                type = "block"
            elif len(active_blocks) > 1:
                type = "lesson"
            return render(request, "class.html", {"sessionDict": sessionDict, "active_blocks": active_blocks, "type": type})

    return redirect("/login/")
          
def details_page(request, class_id):
    if user is not None:
        if user.is_active: 
            print("Details page")
            students = teacher.get_students(class_id)
            return render(request, "details.html", {"sessionDict": sessionDict, "students": students})
    return redirect("/login/")
            
               
                
    return redirect("/login/")

                

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
    response = render(request,'404.html', {"sessionDict": sessionDict})
    response.status_code = 404
    return response


def page_500(request):
    return render(request,'500.html', {"sessionDict": sessionDict})