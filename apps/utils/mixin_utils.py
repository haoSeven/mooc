# _*_ coding:utf-8 _*_

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'haoSev7'
__date__ = '2017/5/18 9:49'


class LoginRequiredMixin(object):
    """
    用户登录认证
    """

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
