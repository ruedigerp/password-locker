#!/usr/bin/env python
from lib.keygen import Keygen
from lib.locker import Locker

from config import locker_path


def print_help():
    print('''Help
    add - adds a new entry
    list - lists all entries
    show - shows a single entry
    exit - exits the program''')


def list_entries(locker):
    print(f'Entries in {locker.name}')
    print('-' * 15)
    if len(locker.library) > 0:
        for entry in locker.library:
            print(entry)
    else:
        print('none')


key = Keygen.get_key()
if key:
    name = input('Provide the name of your locker: ')
    locker = Locker(name, key, locker_path)

    locker.info()

    while True:
        cmd = input(f'({name})> ')
        if cmd.lower() == 'exit':
            break
        elif cmd.lower() == 'list':
            list_entries(locker)
        else:
            print_help()
