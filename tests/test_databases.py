from django.test import SimpleTestCase
from django.urls import reverse, resolve
from herokuapp.models import Attendance, StudentClass, ClassCourses, TeacherCourse, Blocks
from herokuapp.views import login_page, index_page

class TestUrls(SimpleTestCase):
    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_page)
        
    def test_index_url(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index_page)



        