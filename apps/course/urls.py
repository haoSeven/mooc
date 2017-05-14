# _*_ coding:utf-8 _*_

from django.conf.urls import url

from .views import CourseListView, CourseDetailView

__author__ = 'haoSev7'
__date__ = '2017/5/14 0:30'

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
]

