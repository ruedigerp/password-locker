#!/usr/bin/env python
from lib.keygen import Keygen
from lib.crypto import Cipher
from lib.locker import Locker

from config import locker_path

key = Keygen.get_key()
if key:
    # TODO: check if locker already exists in default path (~/.locker.lsf)
    # If no locker exists, create a new one
    # Otherwise load the locker
    name = input('Provide a name for your locker')
    library = Locker(name, key, locker_path)
    library.load()
    library.info()
    library.save()
