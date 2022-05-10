from django.shortcuts import render,redirect,reverse
from homepage.models import ArticleDetailForm,ArticleDetail,ArticleCategory,ArticleCategoryForm
from tittleTattle.models import dailyLog,dailyLogForm
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages
import re
# Create your views here.


def Personal(request):
    context = {}
    articleDetail_form = ArticleDetailForm(initial={"user": request.user,"article_id":0})
    context['articleDetail_form']=articleDetail_form
    context['articleDetail']=ArticleDetail.objects.filter(user=request.user)
    context['articleCount']=ArticleDetail.objects.filter(user=request.user).count()
    context['articleCategoryForm']=ArticleCategoryForm

    year=timezone.now().strftime("%Y")
    context['dailyLog_form']=dailyLogForm(initial={"user": request.user,"year":year,"content_id":0})
    context['dailyLogCount'] = dailyLog.objects.filter(user=request.user).count()
    context['dailyLog'] = dailyLog.objects.filter(user=request.user)

    return render(request,'personal.html',context)

def personalArticle(request):
    data = {}
    articleDetail_form = ArticleDetailForm(data=request.POST)
    if articleDetail_form.is_valid():
        if articleDetail_form.cleaned_data['article_id']==0:
            articleDetail=ArticleDetail()
        else:
            articleDetail = ArticleDetail.objects.get(id=articleDetail_form.cleaned_data['article_id'])
        # articleDetail.avatar=articleDetail_form.cleaned_data['avatar']
        articleDetail.user=articleDetail_form.cleaned_data['user']
        articleDetail.title = articleDetail_form.cleaned_data['title']
        articleDetail.content=articleDetail_form.cleaned_data['content']
        articleDetail.abstract = articleDetail_form.cleaned_data['abstract']
        article_category,create=ArticleCategory.objects.get_or_create(name=articleDetail_form.cleaned_data['category'])
        articleDetail.category =article_category
        articleDetail.status = "p"
        articleDetail.save()
        for i in request.POST.get('tag').split(","):    #标签的添加应该再数据保存到 数据库之后
            articleDetail.tag.add(i)
        data['status']='success'
        data['message'] = "提交成功"
        data['article_id']=articleDetail.id
        data['article_title']=articleDetail.title
        data['create_time'] = articleDetail.create_time.strftime('%y-%m-%d %H:%M:%S')
        data['article_count'] = ArticleDetail.objects.filter(user=request.user).count()
    else:
        data['status']='error'
        data['message']="提交失败"
    return JsonResponse(data)

def updatePersonal(request,number):
    context = {}
    article=ArticleDetail.objects.get(id=number)
    articleDetail_form = ArticleDetailForm(initial={"article_id":article.id,"user": request.user,"content":article.content,"title":article.title,"category":article.category,"abstract":article.abstract})
    context['articleDetail_form']=articleDetail_form
    context['articleDetail']=ArticleDetail.objects.filter(user=request.user)
    return render(request,'personal.html',context)

def deletePersonal(request):
    data = {}
    number=request.GET.get('article_id')
    article = ArticleDetail.objects.get(id=number)
    article.delete()
    article_count=ArticleDetail.objects.filter(user=request.user).count()
    data['article_count']=article_count
    data['article_id'] = number
    data['status']='success'
    return JsonResponse(data)

def personalLog(request):
    data = {}
    dailyLog_form = dailyLogForm(request.POST)
    if dailyLog_form.is_valid():
        if dailyLog_form.cleaned_data['content_id']==0:
            daily_log=dailyLog()
        else:
            daily_log = dailyLog.objects.get(id=dailyLog_form.cleaned_data['content_id'])
        daily_log.user=dailyLog_form.cleaned_data['user']
        daily_log.content = dailyLog_form.cleaned_data['dailyLog']
        daily_log.year = dailyLog_form.cleaned_data['year']

        daily_log.save()

        data['status']='success'
        data['message'] = "提交成功"
        data['daily_log_id']=daily_log.id
        data['daily_log_content'] = re.sub(r'[<p>|</p>]','',daily_log.content)
        data['daily_log_create_time'] = daily_log.create_time.strftime('%y-%m-%d %H:%M:%S')
        data['daily_log_count'] = dailyLog.objects.filter(user=request.user).count()
    else:
        data['status']='error'
        data['message']="提交失败"
    return JsonResponse(data)


def deleteLog(request):
    data = {}
    number=request.GET.get('log_id')
    log = dailyLog.objects.get(id=number)
    log.delete()
    log_count=dailyLog.objects.filter(user=request.user).count()
    data['log_count']=log_count
    data['log_id'] = number
    data['status']='success'
    return JsonResponse(data)


def articleCategory(request):
    data={}
    print(request.POST.get('name'))
    articleCategory=ArticleCategory.objects.get(name=request.POST.get('name'))
    if request.FILES.get('avatar'):
        articleCategory.avatar=request.FILES.get('avatar')

    articleCategory.save()
    messages.error(request,"图片上传成功")
    return HttpResponseRedirect(reverse("personal:personal"))



