from django.shortcuts import render
from .models import LikeNum,LikeNum_cai
from django.db.models import Count,Sum
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from comment.models import G_reviewRecords,reviewRecords
# Create your views here.

def getIPinfo(request):   #获得用户IP地址
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理
    return client_ip

def errorResponse(code,message,id):
    data={}
    data['status']='error'
    data['code']=code
    data['message'] = message
    data['id'] = id
    return JsonResponse(data)

def successResponse(like_sum,id):
    data={}
    data['status']='success'
    if like_sum is None:
        like_sum=0
    data['liked_num']=like_sum
    data['id'] = id
    return JsonResponse(data)

def like_change(request):
    content_type=request.GET.get('content_type')
    model_class=ContentType.objects.get(model=content_type).model_class()
    content_type = ContentType.objects.get_for_model(model_class)
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')
    ip=getIPinfo(request)

    if is_like == 'true':
        likeNum,created=LikeNum.objects.get_or_create(content_type=content_type,object_id=object_id,ip=ip)
        if created:  #created 为 true  说明没有进行过点赞
            likeNum.like_num+=1
            likeNum.save()
        else:        #不能重复点赞
            return errorResponse(402,'已经点赞过',object_id)
    else:
        if not LikeNum.objects.filter(content_type=content_type,object_id=object_id,ip=ip) is None:
            likeNum = LikeNum.objects.get(content_type=content_type, object_id=object_id, ip=ip)
            likeNum.delete()
        else:   #不能重复取消
            return errorResponse(402,'数据错误',object_id)
    result = LikeNum.objects.filter(content_type=content_type, object_id=object_id).aggregate(likeStatistics_sum=Sum('like_num'))
    return successResponse(result['likeStatistics_sum'],object_id)


def cai_like_change(request):
        content_type = request.GET.get('content_type')
        model_class = ContentType.objects.get(model=content_type).model_class()
        content_type = ContentType.objects.get_for_model(model_class)
        object_id = request.GET.get('object_id')
        is_like = request.GET.get('is_like')
        ip = getIPinfo(request)

        if is_like == 'true':
            likeNum, created = LikeNum_cai.objects.get_or_create(content_type=content_type, object_id=object_id, ip=ip)
            if created:  # created 为 true  说明没有进行过点赞
                likeNum.like_num += 1
                likeNum.save()
            else:  # 不能重复点赞
                return errorResponse(402, '已经点赞过',object_id)
        else:
            if not LikeNum_cai.objects.filter(content_type=content_type, object_id=object_id, ip=ip) is None:
                likeNum = LikeNum_cai.objects.get(content_type=content_type, object_id=object_id, ip=ip)
                likeNum.delete()
            else:  # 不能重复取消
                return errorResponse(402, '数据错误',object_id)
        result = LikeNum_cai.objects.filter(content_type=content_type, object_id=object_id).aggregate(likeStatistics_sum=Sum('like_num'))
        return successResponse(result['likeStatistics_sum'],object_id)



