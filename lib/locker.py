import json
import os
import base64
from lib.crypto import Cipher


class Locker:
    def __init__(self, name, key, path):
        self.name = name
        self.path = os.path.expanduser(path)
        self.file_name = f'{self.path}{self.name}.lsf'
        self.key = key
        if not os.path.exists(self.file_name):
            print(f'No locker found in {self.file_name}, creating a new one')
            self.library = {}
            self.save()
        else:
            print(f'Loading locker "{self.file_name}"')
            self.load()

    def load(self):
        encrypted_content = open(self.file_name, 'rb').read()
        try:
            decrypted_content = Cipher.decrypt_message_AES(
                self.key, encrypted_content)
            file_content = json.loads(decrypted_content)
            name = file_content.get('name')
            self.name = name if name else self.name
            self.path = file_content.get('path')
            self.key = base64.b64decode(file_content.get('key'))
            self.library = file_content.get('library')
        except UnicodeDecodeError as e:
            print('Wrong password or your lockerfile is broken')

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        with open(self.file_name, 'wb') as file:
            encrypted_content = Cipher.crypt_message_AES(
                self.key, json.dumps(self.json()))
            file.write(encrypted_content)

    def update_entry(self, name, password, category='password'):
        if not self.library.get(category):
            self.library[category] = {}
        self.library[category][name] = password
        self.save()

    def json(self):
        return {
            'name': self.name,
            'path': self.path,
            'key': base64.b64encode(self.key).decode(),
            'library': self.library
        }

    def info(self):
        print(f'''Library "{self.name}"
  Path: "{self.path}"
  Key Hash: {self.key}''')
