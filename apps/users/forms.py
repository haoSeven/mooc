# _*_ coding:utf-8 _*_

from django import forms

from captcha.fields import CaptchaField

from .models import UserProfile

__author__ = 'haoSev7'
__date__ = '2017/5/2 19:58'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ResetPwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    """
    用于修改头像的表单提交
    继承UserProfile
    """

    class Meta:
        model = UserProfile
        fields = ['image']
