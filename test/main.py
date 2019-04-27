#!/usr/bin/env python
# encoding: utf-8

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: main.py
     @time: 2019-04-27 13:00
"""

from unittest import main, TestCase

from sm4 import SM4Key

try:
    bytes.fromhex
except AttributeError:
    def h2b(byte_string):
        return bytes(bytearray.fromhex(byte_string))
else:
    def h2b(byte_string):
        return bytes.fromhex(byte_string)


class SM4Test(TestCase):
    key = SM4Key(h2b("0123456789abcdeffedcba9876543210"))

    def test_sample(self):
        key = self.key
        plain_text = h2b("0123456789abcdeffedcba9876543210")
        cipher_text = h2b("681edf34d206965e86b3e94f536e4246")
        self.assertEqual(cipher_text, key.encrypt(plain_text))
        self.assertEqual(plain_text, key.decrypt(cipher_text))

    def test_ecb(self):
        key = self.key
        plain_text = b"Encryption is a fantastic world!"
        cipher_text = h2b("8f431932b9ebba90d5aff3a9c973826a2fdcb7392d305b72d5beb7ab86db1227")
        self.assertEqual(cipher_text, key.encrypt(plain_text))
        self.assertEqual(plain_text, key.decrypt(cipher_text))

    def test_cbc(self):
        key = self.key
        initial = b"\0" * 16
        plain_text = b"Encryption is a fantastic world!"
        cipher_text = h2b("8f431932b9ebba90d5aff3a9c973826a98d5b9037a03c4c931bb9485a0d01269")
        self.assertEqual(cipher_text, key.encrypt(plain_text, initial=initial))
        self.assertEqual(plain_text, key.decrypt(cipher_text, initial=initial))

    def test_pcks5(self):
        key = self.key
        plain_text = b"encryption"
        cipher_text = h2b("327ad29fca6983fa31a95fe8051103c7")
        self.assertEqual(cipher_text, key.encrypt(plain_text, padding=True))
        self.assertEqual(plain_text, key.decrypt(cipher_text, padding=True))

    def test_cbc_pcks5(self):
        key = self.key
        initial = b"\0" * 16
        plain_text = b"hi another world"
        cipher_text = h2b("d49702efa235d1d22ed857488e1e81acb0a5f68478f9bf6501eabe251d3507a2")
        self.assertEqual(cipher_text, key.encrypt(plain_text, initial=initial, padding=True))
        self.assertEqual(plain_text, key.decrypt(cipher_text, initial=initial, padding=True))

    def test_pcks5_extra(self):
        key = self.key
        plain_text = b"hi another world"
        cipher_text = h2b("d49702efa235d1d22ed857488e1e81ac002a8a4efa863ccad024ac0300bb40d2")
        self.assertEqual(cipher_text, key.encrypt(plain_text, padding=True))
        self.assertEqual(plain_text, key.decrypt(cipher_text, padding=True))


if __name__ == "__main__":
    main()
