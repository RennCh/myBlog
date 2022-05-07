from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.Login,name='Login'),
    path('register/',views.register,name='register'),
    path('loginout/',views.login_out,name='out'),
]