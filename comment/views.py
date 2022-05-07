from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView,UpdateView
import logging
from .models import reviewRecords,reviewRecordsForm
from django.http import JsonResponse
# Create your views here.

def getIPinfo(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理
    return client_ip
    # ip_exist = reviewRecords.objects.filter(ip=str(client_ip))
    # if ip_exist:  # 判断是否存在该ip
    #     uobj = ip_exist[0]
    #     uobj.count += 1
    # else:
    #     uobj = Userip()
    #     uobj.ip = client_ip
    #     uobj.count = 1
    # uobj.save()

def comment_list(request):
        # commentsDetail = reviewRecords.objects.all()
        commentsDetail=reviewRecords.objects.filter(parent=None).order_by('-create_time')
        reviewRecords_form=reviewRecordsForm(initial={"reply_comment_id":0})
        return render(request,"comments.html",{"commentDetail":commentsDetail,'reviewRecords_form':reviewRecords_form})

def update_comment(request):
        reviewRecords_form=reviewRecordsForm(request.POST)
        data={}
        if reviewRecords_form.is_valid():
            comment=reviewRecords()
            comment.ip=getIPinfo(request)
            reply_comment_id=reviewRecords_form.cleaned_data['reply_comment_id']
            comment.name = reviewRecords_form.cleaned_data['name']
            comment.content = reviewRecords_form.cleaned_data['content']
            parent=reviewRecords_form.cleaned_data['parent']
            if parent is None:
                comment.root=parent
            else:
                if parent.root is None:
                    comment.root = parent
                else:
                    comment.root = parent.root
            comment.parent = parent
            comment.save()

            data["status"]='success'
            data['name']=comment.name
            data['content'] = comment.content
            data['create_time'] = comment.create_time.strftime('%y-%m-%d %H:%M:%S')
            data['ding']=comment.ding
            data['cai']=comment.cai
            data['id']=comment.id
            data['root_id']=comment.root_id
            if comment.parent_id is None:
                data['parent_name']=None
            else:
                data['parent_name']=reviewRecords.objects.get(id=comment.parent_id).name

        else:
            data['error']='error'
            data['message'] = list(reviewRecords_form.errors.values())[0]
        return JsonResponse(data)