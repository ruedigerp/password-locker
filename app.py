#!/usr/bin/env python
from lib.keygen import Keygen
from lib.locker import Locker
from lib.passwordgen import PasswordGenerator
import getpass
from config import locker_path


def print_help():
    print('''Help
    add - adds (or updates) an entry
    gen - generate a new password
    list - lists all entries
    categories - lists all entries
    delete - delete an entry
    delete-category - delete a category
    show - shows a single entry
    exit - exits the program''')


def list_categories(locker):
    print(f'Categories in {locker.name}')
    print('-' * 15)
    if len(locker.library) > 0:
        for category in locker.library:
            print(category)
    else:
        print('none')


def list_entries(locker):
    print(f'Entries in {locker.name}')
    print('-' * 15)
    if len(locker.library) > 0:
        for category in locker.library:
            print(f'- Category "{category}"')
            for entry in locker.library.get(category):
                print('--', entry)
    else:
        print('none')


def add_entry(locker):
    category = input('Category of your entry [password]: ')
    name = input('Name of the entry: ')
    password = getpass.getpass('Password: ')
    if category == '':
        locker.add_entry(name, password)
    else:
        locker.add_entry(name, password, category)
    print(f'Entry {name} saved')


def delete_entry(locker):
    category = input('Category of your entry [password]: ')
    name = input('Name of the entry: ')
    if category == '':
        locker.delete_entry(name)
    else:
        locker.delete_entry(name, category)
    print(f'Entry {name} removed')


def delete_category(locker):
    category = input('Category to delete: ')
    if category != '':
        locker.delete_category(category)
    print(f'Category {category} removed')


def show_entry(locker):
    category = input('Category of your entry [password]: ')
    name = input('Name of the entry: ')
    if category == '':
        entry = locker.get_entry(name)
        category = 'password'
    else:
        entry = locker.get_entry(name, category)
    if entry:
        print(entry.get('password'))
    else:
        print(f'No entry "{name}" found in category "{category}"')


def generate_password():
    password_length = input('Password length [10]: ')
    readable = input('Readable output [Y/n]: ')
    if password_length == '':
        password_length = 10
    else:
        password_length = int(password_length)
    if readable.lower() == 'y' or readable.lower() == '':
        readable = True
    else:
        readable = False
    password = PasswordGenerator.generate_password(password_length, readable)
    print(password)


key = Keygen.get_key()
if key:
    name = input('Provide the name of your locker: ')
    locker = Locker(name, key, locker_path)

    locker.info()

    while True:
        try:
            cmd = input(f'({name})> ')
            if cmd.lower() == 'exit':
                break
            elif cmd.lower() == 'list':
                list_entries(locker)
            elif cmd.lower() == 'categories':
                list_categories(locker)
            elif cmd.lower() == 'add':
                add_entry(locker)
            elif cmd.lower() == 'show':
                show_entry(locker)
            elif cmd.lower() == 'delete':
                delete_entry(locker)
            elif cmd.lower() == 'delete-category':
                delete_category(locker)
            elif cmd.lower() == 'gen':
                generate_password()
            else:
                print_help()
        except EOFError:
            break
