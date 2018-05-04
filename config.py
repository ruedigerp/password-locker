# Locker config

############################################################################
## lock_mode: the way of accessing the locker                             ##
## possible values:                                                       ##
##   quick - checks your master-password from the given type without      ##
##           asking for your password                                     ##
##   safe  - prompts for your password on every access                    ##
############################################################################
lock_mode = 'quick'

############################################################################
## lock_mode: the way of storing your master-password                     ##
## possible values:                                                       ##
##   env   - saves your password in your env as LOCKER_KEY, you are asked ##
##           to export this variable, and saving a line in your shell     ##
##           config after generating your key                             ##
##   file  - saves a .locker_key file in your home directory              ##
############################################################################
lock_type = 'env'

#############################################################################
##  locker_path: the to your password-locker                               ##
##    The ~ or $HOME variable gets expanded so you can refer to your home  ##
##    directory                                                            ##
#############################################################################
locker_path = '~/projects/password-locker/.locker.lsf'
