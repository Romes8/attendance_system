from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from attendance_app.database import get_role, get_courses, history, get_userID


# Create your views here.
def home_page(request, *args, **kwargs):
    print(args, kwargs)
    # print(request.user)  --need for superuser i guess
    return render(request, "layout_base.html", {})


def index_page(request, *args, **kwargs):
    if request.method == 'POST':
        mydict = {}
        print("POST on index")
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = get_role(username, password)
        if not role:
            return render(request, "login.html")
        else:
            mydict['username'] = username
            mydict['role'] = role

            # session data needs to be stored here
            request.session['username'] = username  # ---- for request.session dict there is  a need for database ----
            request.session['role'] = role
            request.session['id'] = get_userID(role, username)

            print(request.session.get('username'))
            print(request.session.get('role'))

            if role == 'teacher':
                data = get_courses(username)
                data = []
                return render(request, "index.html", {'data': data, 'mydict': mydict})
            return render(request, "index.html", {'mydict': mydict})
    else:
        # put procedure here maybe output is different
        rows = {}
        rows['name'] = "Class 1"
        rows['desc'] = "Lorem ipsum this needs to be the description to each card for that card. Make it in database"
        print(rows)
        stats = []

        # for row in rows:
        #   namme = row['name']
        #
        #   stats.append(list((row['name'], row['desc'])))

        # if data want to be extracted from session new dict is needed for it which is passed next
        mydict = {}
        mydict['username'] = request.session.get('username')
        mydict['role'] = request.session.get('role')
        print("GET on index")
        return render(request, "index.html", {'mydict': mydict})


def history_page(request, *args, **kwargs):
    mydict = {'username': request.session.get('username'), 'role': request.session.get('role')}
    data = history(request.session.get('id'), 'date')
    return render(request, "history.html", {"data": data, "mydict": mydict})


def login_page(request, *args, **kwargs):
    # refers to index page and what contect is going to be displayed  when post method is applied
    if request.method == 'GET':
        print("Get method activated")
        return render(request, "login.html")
