from Crypto.Cipher import AES
from Crypto import Random


class Cipher:
    def crypt_message_AES(key, message):
        iv = Random.new().read(AES.block_size)
        obj = AES.new(key, AES.MODE_CFB, iv)
        return iv + obj.encrypt(message)

    def decrypt_message_AES(key, message):
        iv = Random.new().read(AES.block_size)
        obj = AES.new(key, AES.MODE_CFB, iv)
        # don't return iv here, only the message matters
        return obj.decrypt(message)[AES.block_size:].decode()
