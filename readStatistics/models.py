from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
class ReadNum(models.Model):
    read_num=models.IntegerField(default=0)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

class ReadDetail(models.Model):    #不能直接继承 ReadNum  在迁移时会报错
    date=models.DateField(default=timezone.now())
    read_num=models.IntegerField(default=0)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            temp_model = ContentType.objects.get_for_model(self)
            read_num = ReadNum.objects.get(content_type=temp_model, object_id=self.id)
            return read_num.read_num
        except ObjectDoesNotExist:
            return 0
