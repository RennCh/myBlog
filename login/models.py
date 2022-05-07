from django.db import models
from django import forms
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Login_user(forms.Form):
    username=forms.CharField(label="用户名",widget=forms.TextInput(attrs={'class':"input-text",'placeholder':"请输入用户名"}))
    password=forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'class':"input-text",'placeholder':"请输入密码"}))

    # def clean(self):
    #     username=self.cleaned_data['username']
    #     password=self.cleaned_data['password']
    #
    #     user=auth.authenticate(username=username,password=password)
    #     if user == None:
    #         raise forms.ValidationError("用户名或者密码不存在")
    #     else:
    #         self.cleaned_data['user']=user
    #     return self.cleaned_data

    # class Meta:
    #     db_table = "db_login_user"
    #     verbose_name = "用户信息"

class register_user(forms.Form):
    username=forms.CharField(label='用户名',max_length=30,min_length=3,widget=forms.TextInput(attrs={'placeholder':"请输入用户名",'id':'username','name':'username','style':'width:251px;height:32px'}))
    password=forms.CharField(label='密码',max_length=12,min_length=6,widget=forms.PasswordInput(attrs={'placeholder':"请输入密码6-12位",'id':'password','name':'password','style':'width:251px;height:32px'}))
    password_again = forms.CharField(label='确认密码',max_length=12,widget=forms.PasswordInput(attrs={'placeholder':"请再输入密码",'id':'password_again','name':'password_again','style':'width:251px;height:32px'}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'placeholder':"请输入邮箱",'id':'email','name':'email','style':'width:251px;height:32px'}))

    def clean_password_again(self):    #钩子函数  可以给出错误信息
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('邮箱已存在')
        return email
