import logging
import time
from collections import Counter
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView,UpdateView
from .models import ArticleDetail,ArticleCategory
import logging
from django.db.models import Count,Sum,Max,Min
from django.contrib.contenttypes.models import ContentType    #建立通用的阅读量存储
from readStatistics.models import ReadNum,ReadDetail
from comment.models import G_reviewRecords,commentForm
from django.utils import timezone
from django.http import JsonResponse
from tittleTattle.models import dailyLog
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def readStatistics_once_read(request,obj,obj_model):   #博客阅读量增加函数
    temp_model = ContentType.objects.get_for_model(obj_model)
    if not request.COOKIES.get('readed_' + str(obj.id)):
        readNumber, create = ReadNum.objects.get_or_create(content_type=temp_model, object_id=obj.id)
        # if ReadNum.objects.filter(content_type=temp_model,object_id=article.id).count():          #上面一句  等于 下面的if内容
        #     readNumber=ReadNum.objects.get(content_type=temp_model,object_id=article.id)
        # else:
        #     readNumber=ReadNum.objects.create(content_type=temp_model,object_id=article.id)
        readNumber.read_num += 1
        readNumber.save()

        date = timezone.now().date()
        readDetail, create = ReadDetail.objects.get_or_create(date=date, content_type=temp_model, object_id=obj.id)
        readDetail.read_num += 1
        readDetail.save()
    return 'readed_' + str(obj.id)

def readStatistics_threeDay(obj_model):   #统计三天内的 阅读量
    temp_model = ContentType.objects.get_for_model(obj_model)
    today=timezone.now()
    read_nums=[]
    dates=[]
    for i in range(2,-1,-1):
        date=today-timezone.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        result=ReadDetail.objects.filter(content_type=temp_model,date=date).aggregate(readStatistics_sum=Sum('read_num'))
        read_nums.append(result['readStatistics_sum'] or 0)
    return dates,read_nums

def getIPinfo(request):   #获得用户IP地址
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理
    return client_ip

class Home(ListView):
    model=ArticleDetail
    # context_object_name = "article_detail"
    template_name = "articleView.html"
    paginate_by = 5
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self,**kwargs):
        context=super(Home, self).get_context_data(**kwargs)
        # articles=ArticleDetail.objects.all()
        # article_list=[]
        # for article in articles:
        #     article.category_name=ArticleCategory.objects.get(id=article.category_id).name
        #     article_list.append(article)
        # context["page_obj"]=article_list             #向 page_obj 添加额外属性的话  分页功能失效

        # context["category"]=ArticleCategory.objects.all().values_list("name",flat=True)
        articleDetail = ArticleDetail.objects.all()
        context["tags"]=list(set(articleDetail.values_list("tag__name", flat=True)))
        context["tags_count"]=Counter(articleDetail.values_list("tag__name",flat=True))
        dates,read_nums=readStatistics_threeDay(self.model)
        context["dates"]=dates
        context["read_nums"] = read_nums
        context['user']=self.request.user
        context['article_count']=self.model.objects.all().count()
        context['log_count']=dailyLog.objects.all().count()
        return context

def tagList(request):
    articleDetail = ArticleDetail.objects.all()
    if request.method == 'POST':
        tags = list(set(articleDetail.values_list("tag__name", flat=True)))
        search=request.POST.get('search')
        if search:
            articles=articleDetail.filter(Q(title__icontains=search)|Q(content__icontains=search)|Q(abstract__icontains=search))
        else:
            search=''
        context={
            'search':search,
            'articles':articles,
            'tags':tags,
        }
    if request.method == 'GET':
        tag=request.GET.get('tag')
        tags = list(set(articleDetail.values_list("tag__name", flat=True)))
        if tag and tag != 'None':
            article_list = articleDetail.filter(tag__name__in=[tag])
        paginator = Paginator(article_list, 3)
        page = request.GET.get('page')
        # 将导航对象相应的页码内容返回给 articles
        articles = paginator.get_page(page)

        context={
            'articles':articles,
            'tag':tag,
            'tags':tags,
        }
    return render(request,'tagList.html',context)

def update_comment(request):   #每篇文章下面的评论
    # text = request.POST.get("text", '').strip()
    # if text =='':
    #     return render(request,'error.html',{'message':'评论内容不能为空'})
    # try:
    #     ip = getIPinfo(request)
    #     object_id = request.POST.get("object_id", '')
    #     content_type = request.POST.get("content_type", '')
    #     model_class=ContentType.objects.get(model=content_type).model_class()
    # except Exception as e:
    #     return render(request, 'error.html', {'message': '评论对象不存在'})
    #
    # comment=G_reviewRecords()
    # comment.ip=ip
    # comment.object_id=int(object_id)
    # comment.content_type=ContentType.objects.get_for_model(model_class)
    # comment.name='rc'
    # comment.content=text
    # comment.reply=0
    # comment.save()
    #
    # referer=request.META.get('HTTP_REFERER',reverse('homepage:content',kwargs={'number':int(object_id)}))  #反向解析，请求头会有着上一个网页的信息
    # return redirect(referer)
    comment_form=commentForm(request.POST)
    data={}
    if comment_form.is_valid():
        comment = G_reviewRecords()
        ip = getIPinfo(request)
        object_id=comment_form.cleaned_data['object_id']
        #content_type = comment_form.cleaned_data['content_type']
        text = comment_form.cleaned_data['text']
        model_class=comment_form.cleaned_data['model_class']
        content_type=ContentType.objects.get_for_model(model_class)

        parent = comment_form.cleaned_data['parent']
        if parent is None:
            comment.root = parent
        else:
            if parent.root is None:
                comment.root = parent
            else:
                comment.root = parent.root
        comment.parent = parent

        comment.ip=ip
        comment.object_id=int(object_id)
        comment.content_type=content_type
        comment.name=comment_form.cleaned_data['name']
        comment.content=text
        # comment.reply=0
        comment.save()

        # referer = request.META.get('HTTP_REFERER', reverse('homepage:content', kwargs={'number': int(object_id)}))
        #return redirect(referer)
        data['status']='success'
        data['name']=comment.name
        data['create_time']=comment.create_time.strftime('%y-%m-%d %H:%M:%S')
        data['content']=comment.content
        data['cai']=comment.cai
        data['ding']=comment.ding
        data['id']=comment.id

        data['root_id'] = comment.root_id
        if comment.parent_id is None:
            data['parent_name'] = None
        else:
            data['parent_name'] = G_reviewRecords.objects.get(id=comment.parent_id).name

    else:
        data['status']='error'
        data['message']=list(comment_form.errors.values())[0]
    return JsonResponse(data)
        #return render(request, 'error.html', {'message': '评论对象不存在'})



class Article(ListView):    #每篇内容的详细展示
    template_name="articleContent.html"

    def get(self, request,**kwargs):             #  设置cookies
        self.object_list=self.get_queryset()    #   会有报错：缺少 object_list 。使用本行代码可解决
        article=ArticleDetail.objects.get(id=self.kwargs["number"])
        key=readStatistics_once_read(request, article,ArticleDetail)   #利用cookies 文章阅读量增加
        # if not request.COOKIES.get('readed_' + str(article.id)):
        #     temp_model=ContentType.objects.get_for_model(ArticleDetail)
        #     readNumber,create=ReadNum.objects.get_or_create(content_type=temp_model,object_id=article.id)
        #     # if ReadNum.objects.filter(content_type=temp_model,object_id=article.id).count():          #上面一句  等于 下面的if内容
        #     #     readNumber=ReadNum.objects.get(content_type=temp_model,object_id=article.id)
        #     # else:
        #     #     readNumber=ReadNum.objects.create(content_type=temp_model,object_id=article.id)
        #     readNumber.read_num += 1
        #     readNumber.save()
        #
        #     date=timezone.now().date()
        #     readDetail,create=ReadDetail.objects.get_or_create(date=date,content_type=temp_model,object_id=article.id)
        #     readDetail.read_num+=1
        #     readDetail.save()

        response=render(request,self.template_name,self.get_context_data(**kwargs))
        response.set_cookie('readed_' + str(article.id),'true',max_age=60)
        return response

    def get_queryset(self):
        return ArticleDetail.objects.all()

    def get_context_data(self,**kwargs):
        context=super(Article, self).get_context_data(**kwargs)
        article = ArticleDetail.objects.get(id=str(int(self.kwargs["number"])))
        category_id = article.category.id

        now_alterTime=article.alter_time
        maxTime=ArticleDetail.objects.all().aggregate(max_time=Max('alter_time'))
        minTime = ArticleDetail.objects.all().aggregate(min_time=Min('alter_time'))
        if now_alterTime<minTime['min_time']:                      #文章底部 的 上一篇 下一篇的设计
            pre_article=None
            next_article=ArticleDetail.objects.filter(alter_time__lt=article.alter_time).first()
        elif now_alterTime>maxTime['max_time']:
            pre_article = ArticleDetail.objects.filter(alter_time__gt=article.alter_time).last()
            next_article=None
        else:
            pre_article = ArticleDetail.objects.filter(alter_time__gt=article.alter_time).last()
            next_article = ArticleDetail.objects.filter(alter_time__lt=article.alter_time).first()

        content_type=ContentType.objects.get_for_model(article)
        comments=G_reviewRecords.objects.filter(object_id=article.id,content_type=content_type,parent=None)

        context["category"]=ArticleCategory.objects.get(id=category_id).name
        context["article"]=article
        context['pre_article']=pre_article
        context['next_article'] = next_article
        context['comments'] = comments.order_by('-create_time')
        context['content_type']=str(content_type.model)
        context['object_id'] = article.id

        context['comment_form']=commentForm(initial={"object_id":article.id,"content_type":content_type.model,"reply_comment_id":'0'})

        return context


def About(request):
    return render(request,"about.html")

# def informalEssay(request):
#     articles=ArticleDetail.objects.all()
#     logging.error(ArticleDetail.objects)
#     return render(request,"informalEssay.html",{"articles":articles})

class ProgramArticle(ListView):
    model=ArticleDetail
    # context_object_name = "article_detail"
    template_name = "program.html"
    paginate_by = 5
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self,**kwargs):
        context=super(ProgramArticle, self).get_context_data(**kwargs)
        articles_type = ArticleCategory.objects.all()
        articles_type_list = []
        for article_type in articles_type:
            article_type.article_count = ArticleDetail.objects.filter(category_id=article_type.id).count()
            articles_type_list.append(article_type)
        context["category"] = articles_type_list
        context['tags'] = list(set(ArticleDetail.objects.all().values_list("tag__name", flat=True)))
        # context["category"]=ArticleCategory.objects.all().values_list("name",flat=True)
        return context

# class ProgramArticleCategory(ListView):
#     # context_object_name = "article_detail"
#     template_name = "program.html"
#     paginate_by = 5
#
#     def get_queryset(self):
#         return ArticleDetail.objects.all()
#
#     def get_context_data(self,**kwargs):
#         context=super(ProgramArticleCategory, self).get_context_data(**kwargs)
#         category1 = ArticleCategory.objects.filter(name=self.kwargs["number"]).first()
#         article_detail = category1.articledetail_set.all()
#         context["page_obj"]=article_detail                       #分页数据的 替换
#
#         # articles_type=ArticleCategory.objects.all()    #  方法一：每个类别的文章数量
#         # articles_type_list=[]
#         # for article_type in articles_type:
#         #     article_type.article_count=ArticleDetail.objects.filter(category_id=article_type.id).count()
#         #     articles_type_list.append(article_type)
#         # context["category"]=articles_type_list
#
#         context["category"]=ArticleCategory.objects.annotate(article_count=Count('articledetail')) #  方法二：每个类别的文章数量，利用外键
#                            #使用annotate方法 直接增加属性 article_count
#         return context


def ProgramArticleCategory(request,number):
    category1=ArticleCategory.objects.filter(name=number).first()
    articleDetail = category1.articledetail_set.all()
    paginator = Paginator(articleDetail, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    tags = list(set(ArticleDetail.objects.all().values_list("tag__name", flat=True)))
    context = {
        'articles': articles,
        'tags':tags,
        'category':ArticleCategory.objects.annotate(article_count=Count('articledetail')),
    }
    return render(request, 'categoryProgram.html', context)





