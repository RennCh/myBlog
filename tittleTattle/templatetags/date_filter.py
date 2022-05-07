from django.template import Library
from django.contrib.contenttypes.models import ContentType
from likes.models import LikeNum,LikeNum_cai
from django.db.models import Count,Sum
# 将注册类实例化为register对象
register =  Library()


# 使用装饰器注册
@register.filter
def date_sub(val):
    # val为一个列表,通过过滤器取得其中的最大值
    result = int(val)

    return result

@register.filter
def date_sub1(val):
    # val为一个列表,通过过滤器取得其中的最大值
    result = int(val)-1

    return result

@register.filter
def date_sub2(val):
    # val为一个列表,通过过滤器取得其中的最大值
    result = int(val)-2
    return result

@register.filter
def number_add1(val):
    # val为一个列表,通过过滤器取得其中的最大值
    result = int(val)+1
    return result

@register.simple_tag
def likes_sum(obj):
    object_id = obj.id
    content_type = ContentType.objects.get_for_model(obj)
    result = LikeNum.objects.filter(content_type=content_type, object_id=object_id).aggregate(likeStatistics_sum=Sum('like_num'))
    if result['likeStatistics_sum'] is None:
        result['likeStatistics_sum']=0
    return result['likeStatistics_sum']

@register.simple_tag
def cai_likes_sum(obj):
    object_id = obj.id
    content_type = ContentType.objects.get_for_model(obj)
    result = LikeNum_cai.objects.filter(content_type=content_type, object_id=object_id).aggregate(likeStatistics_sum=Sum('like_num'))
    if result['likeStatistics_sum'] is None:
        result['likeStatistics_sum']=0
    return result['likeStatistics_sum']

@register.simple_tag(takes_context=True)
def get_active(obj):
    content_type=ContentType.objects.get_for_model(obj)
    if not LikeNum.objects.filter(content_type=content_type, object_id=obj.id) is None:
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type=ContentType.objects.get_for_model(obj)
    return content_type.model