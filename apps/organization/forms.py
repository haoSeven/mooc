# _*_ coding:utf-8 _*_

import re

from django import forms

from operation.models import UserAsk

__author__ = 'haoSev7'
__date__ = '2017/5/11 16:01'


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        检测输入的手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        p = re.compile(r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$")
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机输入非法', code='mobile_invalid')