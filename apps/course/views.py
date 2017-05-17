# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments


class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-students")[:3]

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by("-fav_nums")
            elif sort == 'students':
                all_courses = all_courses.order_by("-students")

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            "hot_courses": hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 获取与本课程相关的课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
        })


class CommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
        })
