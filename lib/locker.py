import json
import os
import base64
from lib.crypto import Cipher


class Locker:
    def __init__(self, name, key, path):
        self.name = name
        self.path = os.path.expanduser(path)
        self.key = key

    def load(self):
        # encrypted_content = open(self.path, 'rb').read()
        encrypted_content = open(self.path, 'rb').read()
        try:
            decrypted_content = Cipher.decrypt_message_AES(
                self.key, encrypted_content)
            content = json.loads(decrypted_content)
            name = content.get('name')
            self.name = name if name else self.name
            self.path = content.get('path')
            self.key = base64.b64decode(content.get('key'))
            self.content = content.get('content')
        except UnicodeDecodeError as e:
            print('Wrong password or your lockerfile is broken')

    def save(self):
        with open(self.path, 'wb') as file:
            encrypted_content = Cipher.crypt_message_AES(
                self.key, json.dumps(self.json()))
            file.write(encrypted_content)

    def json(self):
        return {
            'name': self.name,
            'path': self.path,
            'key': base64.b64encode(self.key).decode(),
            'content': self.content
        }

    def info(self):
        print(f'''Library "{self.name}"
  Path: "{self.path}"
  Key Hash: {self.key}''')
