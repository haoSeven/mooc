# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import UserFavorite, CourseComments
from course.models import Course
from organization.models import Teacher, CourseOrg


class AddFavView(View):
    """
    机构收藏, 取消收藏
    """
    def post(self, request):
        fav_id = int(request.POST.get("fav_id", 0))
        fav_type = int(request.POST.get("fav_type", 0))

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            # 用户收藏记录已存在，表示用户要取消收藏
            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                if course.fav_nums > 0:
                    course.fav_nums -= 1
                    course.save()
            elif fav_type == 2:
                teacher = Teacher.objects.get(id=fav_id)
                if teacher.fav_nums > 0:
                    teacher.fav_nums -= 1
                    teacher.save()
            elif fav_type == 3:
                org = CourseOrg.objects.get(id=fav_id)
                if org.fav_nums > 0:
                    org.fav_nums -= 1
                    org.save()
            exist_records.delete()
            return HttpResponse('{"status":"fail", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                elif fav_type == 3:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏错误"}', content_type="application/json")


class AddUserCommentView(View):
    """
    添加用户评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comments', "")
        if course_id > 0 and comment:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type="application/json")
