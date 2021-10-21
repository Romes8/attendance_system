from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request, *args, **kwargs):
    print(args,kwargs)
    #print(request.user)  --need for superuser i guess
    return render(request, "layout_base.html", {})

def index_page(request, *args, **kwargs):
    print(args,kwargs)
    #print(request.user)  --need for superuser i guess
    return render(request, "index.html", {})

def login_page(request, *args, **kwargs):
    print(args,kwargs)
    #print(request.user)  --need for superuser i guess
    return render(request, "login.html", {})