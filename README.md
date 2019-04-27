![version](https://img.shields.io/pypi/v/sm4.svg) ![license](https://img.shields.io/pypi/l/sm4.svg)

# SM4
A pure Python implementation for the famous SM4 algorithm, supporting Python 2 and 3.

## Installation
Using `pip`:
```bash
$ pip install sm4 
```

Or manually download the archive and run the command after extracting the stuff inside:
```bash
$ python setup.py install
```

## Usage
Firstly, define a `DesKey` object by passing your encryption / decryption key. The key should be of length 8, 16 or 24. The algorithm will be automatically chosen for you.
Note that the key should be written as `bytes` in *Python 3*.
```python
from sm4 import SM4Key
key0 = SM4Key(b"some key")                  # for DES
key1 = SM4Key(b"a key for TRIPLE")          # for 3DES, same as "a key for TRIPLEa key fo"
key2 = SM4Key(b"a 24-byte key for TRIPLE")  # for 3DES
key3 = SM4Key(b"1234567812345678REAL_KEY")  # for DES, same as "REAL_KEY"
```

Secondly, encrypt messages by calling the method `encrypt()` from the `DesKey` object, or decrypt them by calling `decrypt()`.
Note that the messages should be written as `bytes` in *Python 3*.
```python
key0.encrypt(b"any long message")  # -> b"\x14\xfa\xc2 '\x00{\xa9\xdc;\x9dq\xcbr\x87Q"
```

By default, *ECB Mode* is used. You may enable *CBC Mode* by passing the argument `initial`, as the *Initial Value*.
The argument should be a `bytes` object of length 16. 
```python
key0.encrypt(b"any long message", initial=b"\0"*16)        # -> b"\x14\xfa\xc2 '\x00{\xa9\xb2\xa5\xa7\xfb#\x86\xc5\x9b"
```

The *SM4* algorithm requires the message to be of any length that is a multiple of 16.
By default, the length of the message to encrypt / decrypt is assured by users.
You may choose to turn on *PKCS5 Padding Mode*(by passing the argument `padding` with a TRUTHY value), telling Python to do thg padding before encryption for you.
```python
key0.encrypt(b"abc")  # -> b"%\xd1KU\x8b_A\xa6"
```

While in decryption with *PKCS5 Padding*, the length of the message is still required to be a multiple of 8. But after decryption, Python will throw the padding characters away. 
```python
key0.decrypt(b"%\xd1KU\x8b_A\xa6")  # -> b"abc"
```
