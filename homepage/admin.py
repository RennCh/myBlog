from django.contrib import admin
from .models import ArticleDetail,ArticleCategory


@admin.register(ArticleDetail)
class  ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('id','user','title', 'abstract','content','tag','create_time','alter_time','page_view','category','like_number','get_read_num')


@admin.register(ArticleCategory)
class  ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','create_time','alter_time','avatar')