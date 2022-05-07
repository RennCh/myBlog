import requests
from django.shortcuts import render,redirect,reverse
from login.models import Login_user,register_user
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View
from django import forms
# Create your views here.

def Login(request):
    if request.method == 'POST':
        login_form=Login_user(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect(reverse("homepage:FirstPage"))
            else:
                context = {}
                context['login_form'] = login_form
                context['error_message'] = '用户名或密码错误'
                return render(request, 'login_error.html', context)
        context = {}
        context['login_form'] = login_form
        return render(request, 'login.html', context)
    else:
        login_form=Login_user()
        context={}
        context['login_form']=login_form
        return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        reg_form=register_user(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']

            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            user=auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(reverse("homepage:FirstPage"))
        context = {}
        context['register_form'] = reg_form
        return render(request, 'register.html', context)
    else:
        register_form=register_user()
        context={}
        context['register_form']=register_form
        return render(request,'register.html',context)

def login_out(request):
    auth.logout(request)
    referer=request.META.get('HTTP_REFERER', reverse('homepage:FirstPage'))  # HTTP_REFERER参数可以保留 上一个页面的基本信息
    return redirect(referer)


