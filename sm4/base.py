#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: base.py
  @created: 2019-04-27 13:00
"""

import struct

from .compatibility import iter_range
from .core import derive_keys, encode_block


class SM4Key(object):
    """A class for encryption using SM4 Key"""
    def __init__(self, key):
        self.__encryption_key = guard_key(key)
        self.__decryption_key = self.__encryption_key[::-1]
        self.__key = key

    def encrypt(self, message, initial=None, padding=False):
        """Encrypts the message with the key object.

        :param message: {bytes} The message to be encrypted
        :param initial: {union[bytes, NoneType]} The initial value, using CBC Mode when is not None
        :param padding: {any} Uses PKCS5 Padding when TRUTHY
        :return: {bytes} Encrypted bytes
        """
        return handle(message, self.__encryption_key, initial, padding, 1)

    def decrypt(self, message, initial=None, padding=False):
        """Decrypts the encrypted message with the key object.

        :param message: {bytes} The message to be decrypted
        :param initial: {union[bytes, NoneType]} The initial value, using CBC Mode when is not None
        :param padding: {any} Uses PKCS5 Padding when TRUTHY
        :return: {bytes} Decrypted bytes
        """
        return handle(message, self.__decryption_key, initial, padding, 0)

    def __hash__(self):
        return hash((self.__class__, self.__encryption_key))


def guard_key(key):
    if isinstance(key, bytearray):
        key = bytes(key)

    assert isinstance(key, bytes), "The key should be `bytes` or `bytearray`"
    assert len(key) == 16, "The key should be of length 16"

    return tuple(derive_keys(key))


def guard_message(message, padding, encryption):
    assert isinstance(message, bytes), "The message should be bytes"
    length = len(message)
    if encryption and padding:
        return message.ljust(length + 16 >> 4 << 4, chr(16 - (length & 15)).encode())

    assert length & 15 == 0, (
        "The length of the message should be divisible by 16"
        "(or set `padding` to `True` in encryption mode)"
    )
    return message


def guard_initial(initial):
    if initial is None:
        return

    if isinstance(initial, bytearray):
        initial = bytes(initial)

    assert isinstance(initial, bytes), "The initial value should be of type `bytes` or `bytearray`"
    assert len(initial) & 15 == 0, "The initial value should be of length 16"
    return struct.unpack(">IIII", initial)


def handle(message, key, initial, padding, encryption):
    message = guard_message(message, padding, encryption)
    initial = guard_initial(initial)

    blocks = (struct.unpack(">IIII", message[i: i + 16]) for i in iter_range(0, len(message), 16))

    if initial is None:
        # ECB
        encoded_blocks = ecb(blocks, key)
    else:
        # CBC
        encoded_blocks = cbc(blocks, key, initial, encryption)

    ret = b"".join(struct.pack(">IIII", *block) for block in encoded_blocks)
    return ret[:-ord(ret[-1:])] if not encryption and padding else ret


def ecb(blocks, key):
    for block in blocks:
        yield encode_block(block, key)


def cbc(blocks, key, initial, encryption):
    if encryption:
        for block in blocks:
            data = tuple(x ^ y for x, y in zip(block, initial))
            initial = encode_block(data, key)
            yield initial
    else:
        for block in blocks:
            data = encode_block(block, key)
            initial, block = block, tuple(x ^ y for x, y in zip(data, initial))
            yield block
