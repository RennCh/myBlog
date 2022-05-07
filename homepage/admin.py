from django.contrib import admin
from .models import ArticleDetail


@admin.register(ArticleDetail)
class  ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'content','create_time','alter_time','page_view','get_read_num')