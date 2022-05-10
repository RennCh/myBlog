from django.db import models
from django import forms
from readStatistics.models import ReadNum,ReadNumExpandMethod
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.core.exceptions import ObjectDoesNotExist

from taggit.managers import TaggableManager
# Create your models here.

class ArticleDetail(models.Model,ReadNumExpandMethod):
    STATUS_CHOICES=(
        ("d","Draft"),
        ("p","Publish")
    )

    user= models.CharField(max_length=80,verbose_name="作者")
    title=models.CharField(max_length=80,verbose_name="标题")
    content=RichTextField()
    tag=TaggableManager(blank=True)
    abstract=models.TextField(max_length=50,blank=True,null=True,verbose_name="摘要")
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    alter_time=models.DateTimeField(verbose_name="修改时间",auto_now=True)
    status=models.CharField(max_length=1,choices=STATUS_CHOICES,verbose_name="文章状态")
    is_top=models.BooleanField(verbose_name="置顶",default=False)
    like_number=models.PositiveIntegerField(default=0,verbose_name="点赞数")
    page_view=models.PositiveIntegerField(default=0,verbose_name="阅读量")
    category=models.ForeignKey("ArticleCategory",null=True,on_delete=models.SET_NULL,verbose_name="文章类型")

    class Meta:
        db_table="db_blog_article"
        verbose_name="文章数据表"
        ordering=["-alter_time"]

    def __str__(self):
        return self.title

class ArticleDetailForm(forms.Form):
    article_id=forms.IntegerField(widget=forms.HiddenInput)
    user=forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(widget=forms.TextInput(attrs={"id":"title",'placeholder':"文章标题","style":"float:left"}))
    category = forms.CharField(widget=forms.TextInput(attrs={"id":"category",'placeholder':"文章类别","style":"float:left;margin-left:68px"}))
    abstract = forms.CharField(widget=forms.TextInput(attrs={"id":"abstract",'placeholder':"文章摘要","style":"float:left;margin-left:68px"}))
    tag=forms.CharField(widget=forms.TextInput(attrs={"id":"tag",'placeholder':"文章标签","style":"float:left;margin-left:68px"}))
    content = forms.CharField(widget=CKEditorWidget(config_name='article_ckeditor'))

class ArticleCategory(models.Model):
    name=models.CharField(max_length=50,verbose_name="类名")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    alter_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    avatar =ProcessedImageField(
        upload_to='article/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        default="default.jpg"
    )

    class Meta:
        db_table="db_blog_articlecategory"
        verbose_name="文章类型"
        ordering = ["-alter_time"]
    def __str__(self):
        return self.name

class ArticleCategoryForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"文章类别"}))
    avatar = forms.ImageField()

