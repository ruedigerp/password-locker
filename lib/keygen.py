import os
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib
import getpass
from config import lock_mode, lock_type


class Keygen:
    def generate_key(key=None):
        print(f'Generating new key using lock_mode: "{lock_mode}"')
        if key is None:
            key = Random.new().read(32)  # key size 32 byte to use AES256
        else:
            key = key.encode()
        key = hashlib.sha256(key).digest()
        base64_key = base64.b64encode(key).decode()
        if lock_type == 'env':
            os.environ['LOCKER_KEY'] = f"{base64_key}"
        elif lock_type == 'file':
            open(os.path.expanduser('~/.locker_key'), 'w').write(base64_key)
        print(f'Key generated: {base64_key}')
        print('-' * 25)
        if lock_type == 'env':
            print('Add the following to your shell config (.bashrc/.zshrc/...)')
            print(
                f'\nexport LOCKER_KEY="{base64_key}"\n\nRestart your shell afterwards\n\n')
        elif lock_type == 'file':
            key_path = os.path.expanduser('~/.locker_key')
            print(f'Your keyfile has been generated in {key_path}\n\n')

    def check_key():
        key_input = getpass.getpass('Please enter your master password: ')
        key_input_hash = hashlib.sha256(key_input.encode()).digest()
        base64_key = base64.b64encode(key_input_hash).decode()
        if lock_type == 'env':
            return os.environ.get('LOCKER_KEY') == base64_key
        elif lock_type == 'file':
            return open(os.path.expanduser('~/.locker_key'), 'r').read() == base64_key

    def key_is_available():
        if lock_type == 'env' and os.environ.get('LOCKER_KEY'):
            return True
        elif lock_type == 'file' and os.path.isfile(os.path.expanduser('~/.locker_key')):
            return True
        else:
            return False

    def get_key():
        if Keygen.key_is_available():
            if lock_type == 'env':
                key = os.environ.get('LOCKER_KEY')
            elif lock_type == 'file':
                key = open(os.path.expanduser('~/.locker_key'), 'r').read()
            if lock_mode == 'safe':
                if Keygen.check_key():
                    return base64.b64decode(key)
                else:
                    print('Wrong password')
            else:
                return base64.b64decode(key)
        else:
            phrase = getpass.getpass(
                'No password file found, please provide a new password: ')
            Keygen.generate_key(phrase)
