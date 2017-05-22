# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import UserInfoView, UploadImage, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView

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
    # 我的课程
    url(r'^my_courses/$', MyCourseView.as_view(), name='my_courses'),
    # 我的机构收藏
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='my_fav_org'),
    # 我的教师收藏
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    # 我的教师收藏
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='my_fav_course'),
]
