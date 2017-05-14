# _*_ coding:utf-8 _*_

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner

__author__ = 'haoSev7'
__date__ = '2017/5/1 15:29'


class BaseSetting(object):
    pass


class GlobalSetting(object):
    site_title = "Mooc后台管理"
    site_footer = 'hao'
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)