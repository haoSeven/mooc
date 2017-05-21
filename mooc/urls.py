# _*_ coding:utf-8 _*_
"""mooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView, ModifyView
from operation.views import AddFavView, AddUserCommentView

from mooc.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetView.as_view(), name='forget'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),

    # 用户收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    # 用户评论
    url(r'^add_comment/$', AddUserCommentView.as_view(), name='add_comment'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程url配置
    url(r'^course/', include('course.urls', namespace='course')),

    # 个人信息url配置
    url(r'user/', include('users.urls', namespace='user')),

    # media图像地址 配置上传文件访问地址函数
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
]
