from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
class LikeNum(models.Model):
    like_num=models.IntegerField(default=0)
    like_cai=models.IntegerField(default=0)
    ip=models.CharField(verbose_name='IP地址',max_length=32)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

class LikeNum_cai(models.Model):
    like_num=models.IntegerField(default=0)
    ip=models.CharField(verbose_name='IP地址',max_length=32)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

