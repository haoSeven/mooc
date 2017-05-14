# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from operation.models import UserFavorite
from .forms import UserAskForm


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()

        hot_org = all_org.order_by("-click_nums")[:3]

        # 按城市分类
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        # 按机构划分
        category = request.GET.get('ct', "")
        if category:
            all_org = all_org.filter(category=category)

        # 按学习人数和课程数来分
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_org = all_org.order_by("-student_nums")
            elif sort == 'courses':
                all_org = all_org.order_by("-course_nums")

        all_org_nums = all_org.count()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_org": orgs,
            "all_city": all_city,
            "all_org_nums": all_org_nums,
            "city_id": city_id,
            "category": category,
            "hot_org": hot_org,
            "sort": sort,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"添加错误"}', content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        # 根据页面传递的机构id在数据库中获取相关机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断当前机构是否被该用户收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 取课程机构下所有课程的方法
        all_courses = course_org.course_set.all()[:3]
        # 取课程机构下所有教师的方法
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    """
    机构课程
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断当前机构是否被该用户收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断当前机构是否被该用户收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构教师
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断当前机构是否被该用户收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })
