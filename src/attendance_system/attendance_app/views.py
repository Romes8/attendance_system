from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from attendance_app.database import get_role, get_courses

# Create your views here.
def home_page(request, *args, **kwargs):
    print(args,kwargs)
    #print(request.user)  --need for superuser i guess
    return render(request, "layout_base.html", {})


def index_page(request, *args, **kwargs):
    
    if request.method == 'POST':
        mydict = {}
        print("POST on index")
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = get_role(username, password)
        if role == 0:
            ##error message
            return render(request, "login.html")
        mydict['username'] = username
        mydict['role'] = role

        #session data needs to be stored here
        request.session['username'] = username     # ---- for request.session dict there is  a need for database ----
        request.session['role'] = role

        print(request.session.get('username'))
        print(request.session.get('role'))

        data = []
        if role == 'teacher':
            data = get_courses(username)

        return render(request,"index.html", {'data': data, 'mydict': mydict})
    else:
        #put procedure here maybe output is different
        rows = {}
        rows['name'] = "Class 1"
        rows['desc'] = "Lorem ipsum this needs to be the description to each card for that card. Make it in database"
        print(rows)
        stats = []


        #for row in rows:
         #   namme = row['name']
        #
         #   stats.append(list((row['name'], row['desc'])))


        #if data want to be extracted from session new dict is needed for it which is passed next
        sessiondict = {}
        sessiondict['username'] = request.session.get('username')
        sessiondict['role'] = request.session.get('role')
        print("GET on index")
        return render(request, "index.html", sessiondict)





def login_page(request, *args, **kwargs):
   
   #refers to index page and what contect is going to be displayed  when post method is applied 
    if request.method == 'GET':
        print("Get method activated")
        return render(request, "login.html", {})