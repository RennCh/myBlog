from django.urls import path,re_path,include
from . import views

urlpatterns = [
    path(r'likechange/',views.like_change,name="like_change"),
    path(r'caiLikeChange/',views.cai_like_change,name="cai_like_change"),
]