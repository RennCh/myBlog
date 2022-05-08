from django.db import models
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

# Create your models here.
class dailyLog(models.Model):
    user = models.CharField(max_length=80, verbose_name="作者")
    content=RichTextField()
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    page_view = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    year= models.IntegerField(verbose_name="年份")
    class Meta:
        db_table="db_daillog"
        verbose_name="随笔日常记录"
        ordering=["-create_time"]

class dailyLogForm(forms.Form):
    dailyLog = forms.CharField(widget=CKEditorWidget(config_name='log_ckeditor'))
    user = forms.CharField(widget=forms.HiddenInput)
    year=forms.IntegerField(widget=forms.HiddenInput)
    content_id = forms.IntegerField(widget=forms.HiddenInput)


