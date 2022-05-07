from django.contrib import admin
from comment.models import reviewRecords,G_reviewRecords
# Register your models here.


@admin.register(reviewRecords)
class reviewRecordsAdmin(admin.ModelAdmin):
    list_display = ('ip','name','content','create_time','parent','root')

@admin.register(G_reviewRecords)
class G_reviewRecordsAdmin(admin.ModelAdmin):
    list_display = ('ip','name','object_id','content','create_time','parent','root','content_type')

