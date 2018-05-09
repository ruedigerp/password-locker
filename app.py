#!/usr/bin/env python
from lib.keygen import Keygen
from lib.locker import Locker
from lib.passwordgen import PasswordGenerator
import getpass
import argparse
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


def list_entries(locker, category):
    print(f'- Category "{category}"')
    for entry in locker.library.get(category):
        print('--', entry)


def list_all_entries(locker):
    print(f'Entries in {locker.name}')
    print('-' * 15)
    if len(locker.library) > 0:
        for category in locker.library:
            list_entries(locker, category)
    else:
        print('none')


def add_entry(locker, category=None, name=None, password=None):
    if not category:
        category = input('Category of your entry [password]: ')
    if not name:
        name = input('Name of the entry: ')
    if not password:
        password = getpass.getpass(f'Password for entry {name}: ')
    if category == '':
        locker.add_entry(name, password)
    else:
        locker.add_entry(name, password, category)
    print(f'Entry {name} saved in category {category}')


def delete_entry(locker, category=None, name=None):
    if not category:
        category = input('Category of your entry [password]: ')
    if not name:
        name = input('Name of the entry: ')
    if category == '':
        locker.delete_entry(name)
    else:
        locker.delete_entry(name, category)
    print(f'Entry {name} removed from category {category}')


def delete_category(locker, category=None):
    if not category:
        category = input('Category of your entry [password]: ')
    if category != '':
        locker.delete_category(category)
    print(f'Category {category} removed')


def show_entry(locker, category=None, name=None):
    if not category:
        category = input('Category of your entry [password]: ')
    if not name:
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


def generate_password(password_length=None, readable=None):
    if not password_length:
        password_length = input('Password length [10]: ')
    if readable is None:
        readable = input('Readable output [Y/n]: ')
        if readable.lower() == 'y' or readable.lower() == '':
            readable = True
        else:
            readable = False
    if password_length == '':
        password_length = 10
    else:
        password_length = int(password_length)
    password = PasswordGenerator.generate_password(password_length, readable)
    return password


parser = argparse.ArgumentParser()
parser.add_argument('LOCKER', help='Name of the locker to use')
parser_group = parser.add_mutually_exclusive_group()
parser_group.add_argument('-a', '--add', metavar='ENTRY',
                          dest='ADD_ENTRY', help='Add a new entry')
parser.add_argument('-c', '--category', dest='CATEGORY',
                    help='Category to use (defaults to "password")')
parser.add_argument('-g', '--generate', action='store_true',
                    help='Generate a password')
parser.add_argument('--length', dest='LENGTH',
                    help='Length of the generated password', default='10')
parser.add_argument('--readable', action='store_true',
                    help='Make the generated password readable', default=False)
parser_group.add_argument(
    '-d', '--delete', metavar='ENTRY', dest='DELETE_ENTRY', help='Delete an entry')
parser.add_argument(
    '-dc', '--delete-category', action='store_true', help='Delete a category')
parser_group.add_argument(
    '-l', '--list', action='store_true', help='List entries')
parser_group.add_argument('-lc', '--list-categories',
                          action='store_true', help='List categories')
parser_group.add_argument('-r', '--read', metavar='ENTRY',
                          dest='READ_ENTRY', help='Retrieve an entry')

args = parser.parse_args()
key = Keygen.get_key()
if key:
    locker = Locker(args.LOCKER, key, locker_path)
    if args.ADD_ENTRY:
        category = args.CATEGORY if args.CATEGORY else 'password'
        password = None
        if args.generate:
            password = generate_password(
                password_length=args.LENGTH, readable=args.readable)
        add_entry(locker, name=args.ADD_ENTRY,
                  category=category, password=password)
    elif args.DELETE_ENTRY:
        category = args.CATEGORY if args.CATEGORY else 'password'
        delete_entry(locker, name=args.DELETE_ENTRY, category=category)
    elif args.READ_ENTRY:
        category = args.CATEGORY if args.CATEGORY else 'password'
        show_entry(locker, name=args.READ_ENTRY, category=category)
    elif args.list:
        if args.CATEGORY:
            list_entries(locker, category=args.CATEGORY)
        else:
            list_all_entries(locker)
    elif args.list_categories:
        list_categories(locker)
    elif args.delete_category:
        category = args.CATEGORY if args.CATEGORY else 'password'
        delete_category(locker, category=category)
    elif args.generate:
        print(generate_password(password_length=args.LENGTH, readable=args.readable))
    else:
        while True:
            try:
                cmd = input(f'({args.LOCKER})> ')
                if cmd.lower() == 'exit':
                    break
                elif cmd.lower() == 'list':
                    list_all_entries(locker)
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
                    print(generate_password())
                else:
                    print_help()
            except EOFError:
                break
