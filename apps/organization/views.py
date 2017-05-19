# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from .forms import UserAskForm
from course.models import Course


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()

        hot_org = all_org.order_by("-click_nums")[:3]

        # 机构搜索
        kw = request.GET.get('keywords', '')
        if kw:
            all_org = all_org.filter(Q(name__icontains=kw) | Q(desc__icontains=kw))

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


class TeacherListView(View):
    """
    教师列表页
    """

    def get(self, request):
        # 取出所有的教师
        all_teachers = Teacher.objects.all()
        # 对所有的教师进行倒序排序，选出收藏量最高的3个，显示为热门推荐
        hot_list = all_teachers.order_by('-fav_nums')[:3]

        # 教师搜索
        kw = request.GET.get('keywords', '')
        if kw:
            all_teachers = all_teachers.filter(Q(name__icontains=kw) | Q(work_company__icontains=kw))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-fav_nums')

        # 显示取出来的教师数量
        all_teachers_nums = all_teachers.count()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'all_teachers_nums': all_teachers_nums,
            'hot_list': hot_list,
            'sort': sort,
        })


class TeacherDetailView(View):
    """
    教师详情页
    """

    def get(self, request, teacher_id):
        # 根据穿过来的id取出对应的教师
        teacher = Teacher.objects.get(id=teacher_id)

        # 教师点击数加一
        teacher.click_nums += 1
        teacher.save()

        has_teacher_fav = False
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_fav = True
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True

        # 查找该教师所有的课程
        all_courses = Course.objects.filter(teacher=teacher)
        # 根据收藏的数量对所有的教师进行排序，取出前3个
        sort_teachers = Teacher.objects.all().order_by("-fav_nums")[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sort_teachers': sort_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,
        })
