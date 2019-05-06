# -*- coding:utf-8 -*-
# To do fix password issue
import base64


class User(object):

    def __init__(self, uid):
        self._uid = uid
        self.userName = ""
        self._upassword = ""
        self._mobile = ""
        self._mpassword = ""
        self._email = ""
        self._epassword = ""

    @property
    def userName(self):
        return self.userName

    @userName.setter
    def userName(self, value):
        self._userName = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        self._mobile = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def upassword(self):
        return self._upassword

    @upassword.setter
    def upassword(self, value):

        self._upassword = base64.b64decode(value)

    @property
    def mpassword(self):
        return self._mpassword

    @mpassword.setter
    def mpassword(self, value):
        self._mpassword = base64.b64decode(value)

    @property
    def epassword(self):
        return self._epassword

    @epassword.setter
    def epassword(self, value):
        self._epassword = base64.b64decode(value)
# Base64编码是一种“防君子不防小人”的编码方式。
# 广泛应用于MIME协议，作为电子邮件的传输编码，生成的编码可逆，后一两位可能有“=”，生成的编码都是ascii字符。
# 速度快，ascii字符，肉眼不可理解，但仅适用于加密非关键信息的场合