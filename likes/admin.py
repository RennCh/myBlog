from django.contrib import admin
from .models import LikeNum,LikeNum_cai
# Register your models here.
@admin.register(LikeNum)
class  LikeNumAdmin(admin.ModelAdmin):
    list_display = ('id','like_num','like_cai','ip','object_id','content_type','content_object')

@admin.register(LikeNum_cai)
class  LikeNum_caiAdmin(admin.ModelAdmin):
    list_display = ('id','like_num','ip','object_id','content_type','content_object')