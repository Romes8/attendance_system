from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from attendance_app.database import get_role, get_courses, history, get_userID_name
sessionDict = {}
wrongLogin = 'false' #variable for error diplay message while logging in 

# Create your views here.
def home_page(request, *args, **kwargs):
    print(args, kwargs)
    return redirect("/login/", {})


def index_page(request, *args, **kwargs):
    global wrongLogin

    if request.method == 'POST':
        wrongLogin = 'false'  #set login check back to deafault
        print("POST on index")
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        role = get_role(username, password)
        if not role:
           
            wrongLogin = 'true'
            print(wrongLogin)
            return redirect("/login/")
        else:
            global sessionDict#
            # session data needs to be stored here
            request.session['login'] = "True"
            request.session['username'] = username  
            request.session['role'] = role
            request.session['id'], name = get_userID_name(role, username)
            request.session.set_expiry(1200)

            sessionDict['username'] = request.session.get('username')
            sessionDict['role'] = request.session.get('role')
            sessionDict['id'] = request.session.get('id')
            sessionDict['name'] = name

            print(request.session.get('username'))
            print(request.session.get('role'))
            print(request.session.get('login'))

            if role == 'teacher':
                data = []
                data = get_courses(sessionDict['id'])
                
                return render(request, "index.html", {'data': data, 'sessionDict': sessionDict})
            return render(request, "index.html", {'sessionDict': sessionDict})
    else:
        wrongLogin = 'false'  #set login check back to deafault

        if request.session.get('login') == "True":
            print("Logged in")
        else:
            print("Not loggen in")
            return redirect("/login/", {})
       
        print("GET on index")
        return render(request, "index.html", {'sessionDict': sessionDict})


def history_page(request, *args, **kwargs):
    data = history(sessionDict['id'], 'date')
    return render(request, "history.html", {"data": data, "sessionDict": sessionDict})


def login_page(request, *args, **kwargs):

    # refers to index page and what contect is going to be displayed  when post method is applied
    if request.method == 'GET':
        print("Get method activated")
        return render(request, "login.html", {'wrongLogin': wrongLogin}) #sending message for wrong login

def logout_page(request):
    try:
        del request.session['login']
        sessionDict.clear()
        print(sessionDict)
    except KeyError:
        pass
    return redirect("/login/", {})
