from django.urls import path
from .views import Alert_ListView, package_detection, Alert_DeleteView, User_LoginView, User_Registration
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', User_LoginView.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(next_page='Login'), name='Logout'),
    path('register/', User_Registration.as_view(), name='Register'),
    path("", Alert_ListView.as_view(), name="Alerts"),
    path("package-detection/", package_detection, name='Package Detection'),
    path('Alert/<int:pk>/', Alert_DeleteView.as_view(), name='Delete' ),
]