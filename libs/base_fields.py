#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz



from Crypto import Random
from django.db import models
from django.conf import settings
import ast

from  Crypto.Cipher import AES


class ListField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value
        print(type(value))
        print(value)
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return ast.literal_eval(value)


from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class SimpleCrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0'.encode())


class AESCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        if 'prefix' in kwargs:
            self.prefix = kwargs['prefix']
            del kwargs['prefix']
        else:
            self.prefix = 'aes_str:::'
        self.aes_encrypt = SimpleCrypt(settings.SECRET_KEY_FOR_AES)
        super(AESCharField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AESCharField, self).deconstruct()
        if self.prefix != "aes_str:::":
            kwargs["prefix"] = self.prefix
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        if value.startswith(self.prefix):
            value = value[len(self.prefix):]
            value = self.aes_encrypt.decrypt(value)
        return value.decode()

    def to_python(self, value):
        if value is None:
            return value
        elif value.startswith(self.prefix):
            value = value[len(self.prefix):]
            value = self.aes_encrypt.decrypt(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, str):
            value = self.aes_encrypt.encrypt(value)
            value = self.prefix.encode("utf-8") + value
        elif value is not None:
            raise TypeError(str(value)) + "is not a valid value for AESCharField"
        return value
