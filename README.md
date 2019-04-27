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
Firstly, define a `SM4Key` object by passing your encryption / decryption key. The key should be of length 16.
Note that the key should be written as `bytes` in *Python 3*.
```python
from sm4 import SM4Key
key0 = SM4Key(b"any length16 key")
```

Secondly, encrypt messages by calling the method `encrypt()` from the `SM4Key` object, or decrypt them by calling `decrypt()`.
Note that the messages should be written as `bytes` in *Python 3*.
```python
key0.encrypt(b"Any very very very long message!")  # -> b'\x15\x8a\x18_qg\xf4%\x080\xb2HEFFO\x90\x0e\xc1\xbb\x07\xe5\xae\xed\xd5\x90\xf4K\xfb\xae]\xae'
```

By default, *ECB Mode* is used. You may enable *CBC Mode* by passing the argument `initial`, as the *Initial Value*.
The argument should be a `bytes` object of length 16. 
```python
key0.encrypt(b"any long message", initial=b"\0"*16)        # -> b'\x15\x8a\x18_qg\xf4%\x080\xb2HEFFO\x98\x01}1\xe3\xa5oL\xdf\x95(A\xd8\xce\x14\xc9'
```

The *SM4* algorithm requires the message to be of any length that is a multiple of 16.
By default, the length of the message to encrypt / decrypt is assured by users.
You may choose to turn on *PKCS5 Padding Mode*(by passing the argument `padding` with a TRUTHY value), telling Python to do the padding before encryption for you.
```python
key0.encrypt(b"abc", padding=True)  # -> b'K\x9euZ\x03\x96\xe0\x93+\xc9%Z\xab\xf5\xff\x17'
```

While in decryption with *PKCS5 Padding*, the length of the message is still required to be a multiple of 8. But after decryption, Python will throw the padding characters away. 
```python
key0.decrypt(b"K\x9euZ\x03\x96\xe0\x93+\xc9%Z\xab\xf5\xff\x17", padding=True)  # -> b"abc"
```
