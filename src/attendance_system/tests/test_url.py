from django.test import SimpleTestCase
from django.urls import reverse, resolve
from attendance_app.views import index_page, login_page, logout_page, history_page

class TestUrls(SimpleTestCase):

    def test_index_page(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index_page)

    def test_login_page(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_page)

    def test_logout_page(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_page)

    def test_history_page(self):
        url = reverse('history')
        self.assertEquals(resolve(url).func, history_page)