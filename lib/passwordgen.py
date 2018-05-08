#!/usr/bin/env python
import string
import random
import textwrap

class PasswordGenerator:
    def generate_password(password_length=10, readable=True, special_chars='-_!?#$'):
        generated_password = ''
        if readable:
            password_range = string.ascii_lowercase
        else:
            password_range = string.ascii_letters + string.digits + special_chars
        for _ in range(password_length):
            generated_password += random.choice(password_range)

        if readable:
            password_chunks = textwrap.wrap(generated_password, 3)
            password = '-'.join(password_chunks)
        else:
            password = generated_password
        return password


if __name__ == '__main__':
    print('10, readable', PasswordGenerator.generate_password())
    print('20, readable', PasswordGenerator.generate_password(20))
    print('20, non-readable', PasswordGenerator.generate_password(20, False))
    print('13, non-readable, special-chars',
          PasswordGenerator.generate_password(20, False, '#@!§$%&)(]?!*+)'))
