from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView,UpdateView
from .models import dailyLog
import logging
import time
# Create your views here.

def informalEssay(request):
    year_now=time.strftime("%Y",time.localtime(time.time()))
    # articles=dailyLog.objects.all()
    articles1=dailyLog.objects.filter(create_time__year=year_now)
    articles2 = dailyLog.objects.filter(create_time__year=str(int(year_now)-1))
    articles3 = dailyLog.objects.filter(create_time__year=str(int(year_now) - 2))
    articles4 = dailyLog.objects.filter(create_time__year=str(int(year_now) - 3))
    return render(request,"informalEssay.html",{"articles1":articles1,"articles2":articles2,"articles3":articles3,"articles4":articles4})