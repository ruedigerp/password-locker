## Installation

    git clone https://github.com/sambadevi/password-locker
    cd password-locker
    pip3 install -r requirements.txt

## How to Use

### add new entry

    #> python3 app.py MyPasswords -c Internet -a web.de
    No locker found in /Users/rpr/password-locker/MyPasswords.lsf, creating a new one
    Password for entry web.de:
    Entry web.de saved in category Internet

### Show all entries

    #> python3 app.py MyPasswords -c Internet -l
    - Category "Internet"
    -- web.de

### Show one entry

    #> python3 app.py MyPasswords -c Internet -r web.de
    foobar

### Change password

    #> python3 app.py MyPasswords -c Internet -a web.de
    Password for entry web.de:
    Entry web.de saved in category Internet

### List categories

    #> python3 app.py MyPasswords -lc
    Categories in MyPasswords
    ---------------
    Internet

### Generate Password

    #> python3 app.py MyPasswords -c Internet -a web.de -g --length 20
    Entry web.de saved in category Internet

### Show Password

    #> python3 app.py MyPasswords -c Internet -r web.de
    DklTxu4LyXVN7v$6UjOF
