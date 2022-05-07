from django.urls import path,re_path,include
from . import views
urlpatterns = [
    path('',views.Home.as_view(),name="FirstPage"),
    path(r'content/(?P<number>\d+)',views.Article.as_view(),name="content"),
    path(r'content/comment/)',views.update_comment,name="comment"),
    path('about/',views.About,name="about"),
    path('program/',views.ProgramArticle.as_view(),name="program"),
    path(r'program/(?P<number>\.+)',views.ProgramArticleCategory,name="programCategory"),
    path('tagList/', views.tagList, name="tagList"),
]