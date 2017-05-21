# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import UserInfoView, UploadImage, UpdatePwdView, SendEmailCodeView, UpdateEmailView

__author__ = 'haoSev7'
__date__ = '2017/5/21 14:24'

urlpatterns = [
    # 用户个人信息页面
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 修改头像
    url(r'^upload/image/$', UploadImage.as_view(), name='upload_image'),
    # 修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
]
