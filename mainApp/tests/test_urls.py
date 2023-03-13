from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import User_LoginView, LogoutView, User_Registration, Alert_ListView, package_detection, Alert_DeleteView
from django.contrib.auth.views import LogoutView


# Test url resolves
class TestUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('Login')
        self.assertEquals(resolve(url).func.view_class, User_LoginView)

    def test_logout_url_resolves(self):
        url = reverse('Logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_register_url_resolves(self):
        url = reverse('Register')
        self.assertEquals(resolve(url).func.view_class, User_Registration)

    def test_alerts_url_resolves(self):
        url = reverse('Alerts')
        self.assertEquals(resolve(url).func.view_class, Alert_ListView)

    def test_package_detection_url_resolves(self):
        url = reverse('Package Detection')
        self.assertEquals(resolve(url).func, package_detection)

    def test_alert_delete_url_resolves(self):
        url = reverse('Delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, Alert_DeleteView)