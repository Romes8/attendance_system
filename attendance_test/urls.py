"""attendance_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from herokuapp.views import change_pass, forgot_pass, student_details, details_page, check_code, active_class, home_page, index_page, login_page, history_page, logout_page, settings_page, class_selected

handler404 = "herokuapp.views.page_404"
handler500 = "herokuapp.views.page_500"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('index/', index_page, name='index'),
    path('login/',login_page, name='login'),
    path('history/', history_page, name='history'),
    path('logout/', logout_page, name='logout'),
    path('settings/', settings_page, name='settings'),
    path('code_send/', check_code),
    path('block/<int:teacher_course>/', active_class, name='activate class'),
    path('class/<int:class_course>/', class_selected, name="class selected"),
    path('details/<int:teacher_course>/<int:class_id>/', details_page, name='details_page'),
    path('student/<int:teacher_course>/<int:student_id>/', student_details),
    path('forgotpass/', forgot_pass),
    path('changepass/', change_pass)
]