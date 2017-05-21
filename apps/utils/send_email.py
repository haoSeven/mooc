# _*_ coding:utf-8 _*_
from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail

from mooc.settings import EMAIL_FROM

__author__ = 'haoSev7'
__date__ = '2017/5/3 16:24'


def random_str(randlen=8):
    strs = ''
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randlen):
        strs += chars[random.randint(0, length)]

    return strs


def send_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "Mooc学习网激活链接"
        email_body = "请点击下列链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status == 1:
            pass
    elif send_type == 'forget':
        email_title = "Mooc学习网重置密码链接"
        email_body = "请点击下列链接重置用户密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status == 1:
            pass
    elif send_type == 'update_email':
        email_title = "Mooc学习网修改个人邮箱"
        email_body = "{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status == 1:
            pass



