#!/usr/bin/env python
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
import os
import sys
import binascii


def crypt_message_AES(key, message):
    iv = Random.new().read(AES.block_size)
    obj = AES.new(key, AES.MODE_CFB, iv)
    return iv + obj.encrypt(message)
    
def decrypt_message_AES(key, message):
    iv = Random.new().read(AES.block_size)
    obj = AES.new(key, AES.MODE_CFB, iv)
    return obj.decrypt(message)[AES.block_size:]


key = os.environ.get('LOCKER_KEY')
if key:
    if sys.argv[1] == 'crypt':
        print(crypt_message_AES(key, sys.argv[2]))
    elif sys.argv[1] == 'decrypt':
        print(decrypt_message_AES(key, sys.argv[2]).decode('utf-8'))
