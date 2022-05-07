from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.Personal,name='personal'),
    path(r'updatePersonal/(?P<number>\d+)',views.updatePersonal,name='updatePersonal'),
    path(r'deletePersonal/',views.deletePersonal,name='deletePersonal'),
    path('personalArticle/',views.personalArticle,name='personalArticle'),
    path('personalLog/',views.personalLog,name='personalLog'),
    path('deleteLog/',views.deleteLog,name='deleteLog'),

    path('articleCategory/', views.articleCategory, name="articleCategory"),
]