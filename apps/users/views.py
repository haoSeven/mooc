# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from users.models import UserProfile, EmailVerifyRecord
from users.forms import LoginForm, RegisterForm, ForgetForm, ResetPwdForm, UploadImageForm
from utils.send_email import send_email
from utils.mixin_utils import LoginRequiredMixin

__all__ = [
    'CustomBackend',
    'ActiveUserView',
    'RegisterView',
    'LoginView',
    'ForgetView',
    'ResetView',
    'ModifyView',
    'UserInfoView',
    'UploadImage',
]


class CustomBackend(ModelBackend):
    """
    修改账号验证逻辑，用户名与邮箱都可以用于登录
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    """
    用户激活账号
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {"register_form": register_form, "msg": "用户已经存在"})
            password = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)
            user_profile.save()

            send_email(username, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {"msg": u"用户未激活"})
            else:
                return render(request, 'login.html', {"msg": u"用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class ForgetView(View):

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_email(email, "forget")
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    """
    密码重置页面
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyView(View):
    """
    密码修改
    """

    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            pwd = request.POST.get("password", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg": "两次密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "reset_form": reset_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息页面
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })


class UploadImage(LoginRequiredMixin, View):
    """
    修改头像
    使用form.ModelForm表单方式对上传的图片做保存
    """

    def post(self, request):
        # ModelForm : instance 接收一个已经存在的模型实例；如果提供，save() 将更新这个实例
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")
