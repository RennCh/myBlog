from django.db import models
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

# Create your models here.


class reviewRecords(models.Model):
    ip=models.CharField(verbose_name='IP地址',max_length=32)
    name = models.CharField(max_length=20,verbose_name="匿名")
    content=RichTextField()
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    ding=models.IntegerField(verbose_name="顶",default=0)
    cai = models.IntegerField(verbose_name="踩",default=0)
    parent=models.ForeignKey('self',null=True,related_name="parent_comment",on_delete=models.CASCADE)   #与自己建立外键
    root=models.ForeignKey('self', null=True,related_name="root_comment", on_delete=models.CASCADE)

    class Meta:
        db_table = "db_reviewRecords"
        verbose_name = "评论记录"
        ordering = ["create_time"]

class reviewRecordsForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={"id":"comment_name",'placeholder':"请留下你的匿名"}))
    content=forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))
    reply_comment_id=forms.IntegerField(widget=forms.HiddenInput(attrs={"id":"reply_comment_id"}))
    def clean(self):
        name=self.cleaned_data['name']
        if name == '':
            raise forms.ValidationError("匿名不能为空")
        return self.cleaned_data
    def clean_reply_comment_id(self):
        reply_comment_id=self.cleaned_data['reply_comment_id']
        if reply_comment_id<0:
            raise forms.ValidationError("回复出错")
        elif reply_comment_id==0:
            self.cleaned_data['parent']=None
        elif reviewRecords.objects.filter(id=reply_comment_id).exists():
            self.cleaned_data['parent']=reviewRecords.objects.get(id=reply_comment_id)
        else:
            raise forms.ValidationError("回复出错")
        return reply_comment_id


class G_reviewRecords(models.Model):

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    ip=models.CharField(verbose_name='IP地址',max_length=32)
    name = models.CharField(max_length=20,verbose_name="匿名")
    content=models.TextField(verbose_name="内容")
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    ding=models.IntegerField(verbose_name="顶",default=0)
    cai = models.IntegerField(verbose_name="踩",default=0)
    parent=models.ForeignKey('self',null=True,related_name="parent_comment",on_delete=models.CASCADE)   #与自己建立外键
    root=models.ForeignKey('self', null=True,related_name="root_comment", on_delete=models.CASCADE)

    class Meta:
        db_table = "db_G_reviewRecords"
        verbose_name = "通用_评论记录"
        ordering = ["create_time"]

class commentForm(forms.Form):
    object_id=forms.IntegerField(widget=forms.HiddenInput)
    content_type=forms.CharField(widget=forms.HiddenInput)
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={"id": "reply_comment_id"}))
    name=forms.CharField(widget=forms.TextInput(attrs={"id":"comment_name",'placeholder':"请留下你的匿名"}))
    text=forms.CharField(widget=forms.Textarea(attrs={"id":"text","class":"form-control","rows":4,'placeholder':"留下你的评论"}))

    def clean(self):
        content_type = self.cleaned_data["content_type"]
        object_id = self.cleaned_data["object_id"]
        content = self.cleaned_data["text"]
        if content == '':
            raise forms.ValidationError("评论不能为空")
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
          #  mdoel_obj=model_class.objects.get(id=object_id)
            self.cleaned_data['model_class']=model_class
        except ObjectDoesNotExist:
            raise forms.ValidationError("评论对象不存在")
        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id=self.cleaned_data['reply_comment_id']
        if reply_comment_id<0:
            raise forms.ValidationError("回复出错")
        elif reply_comment_id==0:
            self.cleaned_data['parent']=None
        elif G_reviewRecords.objects.filter(id=reply_comment_id).exists():
            self.cleaned_data['parent']=G_reviewRecords.objects.get(id=reply_comment_id)
        else:
            raise forms.ValidationError("回复出错")
        return reply_comment_id
