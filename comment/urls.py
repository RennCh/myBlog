from django.urls import path,re_path,include
from . import views
urlpatterns = [
    path('',views.comment_list,name='commentList'),
    path(r'update/',views.update_comment,name='updateComment'),
]