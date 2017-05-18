# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


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


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了本课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 如果用户还未学习过本课程
        if not user_courses:
            # 向用户课程表中关联用户与本课程
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 根据这门课程在用户课程表中查找出所有学习过这门课的用户实体
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有学习了本课程的用户实体的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据id取出学习了本课程的用户学习过的其他课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 根据all_user_courses 取出所有的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据学习了本课程的用户学习过的课程id在课程表中取出所有的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-students")[:5]

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })


class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
        })
