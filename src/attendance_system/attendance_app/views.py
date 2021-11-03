from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import SESSION_KEY, login, logout
import attendance_app.database as database
from attendance_app.database import activate_block, settings, get_role, get_courses, history, get_userID_name
from attendance_app.models import DjangoSession, Login
from datetime import datetime, timedelta
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
            sessionDict['id'], sessionDict['name'] = get_userID_name(sessionDict['role'], sessionDict['username'])
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
            if sessionDict['role'] == 'teacher':
                data = get_courses(sessionDict['id'])
                return render(request, "index.html", {'sessionDict': sessionDict, 'data': data})
            return render(request, "index.html", {'sessionDict': sessionDict})
    else:
        return redirect('/login/')

def history_page(request):
    if user is not None:
        if user.is_active:
            if sessionDict['role'] == 'student':
                data = history(sessionDict['id'], 'date')
                return render(request, "history.html", {"data": data, "sessionDict": sessionDict})
            else:
                redirect('/index/')
    else:
        return redirect('/login/')

def settings_page(request):
    if user is not None:
        if user.is_active:
            if sessionDict['role'] == 'teacher':
                data = settings(sessionDict['id'])
                return render(request, "settings.html", {'sessionDict': sessionDict, 'data': data})
            else:
                return redirect('/index/')
    else:
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

def extend_session(request):
    print(request.POST)
    
    return True
# check for the right wifi connection 

if "Vartic2" in subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8'):
    print('good network')