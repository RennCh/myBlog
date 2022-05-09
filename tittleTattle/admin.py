from django.contrib import admin
from .models import dailyLog
# Register your models here.

@admin.register(dailyLog)
class  dailyLogAdmin(admin.ModelAdmin):
    list_display = ('id','user','content','create_time','page_view','year')
