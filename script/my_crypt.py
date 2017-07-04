#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，文本text必须为16的倍数，需补足
    def encrypt(self, text):
        if text is None:
            return ''
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、32（AES-256）
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，
        # 输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

mycrypt = prpcrypt('jmgao123jmgao123')

if __name__ == '__main__':
    pc = prpcrypt('douniwandouniwan')
    e = pc.encrypt("jmCW3vlA;RkJ,")
    d = pc.decrypt(e)
    print(e + "--密文")
    print(d + "--原文")
