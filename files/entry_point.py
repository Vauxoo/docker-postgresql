#!/usr/bin/python

from os import listdir, stat, chown, path
from subprocess import Popen, call
import pwd

POSTGRES_PATH = '/var/lib/postgresql'
POSTGRES_CONFIG = '/etc/postgresql'

def get_owner(file_name):
    '''
    This function gets owner name from system for a directory or file

    :param str file_name: File or directory name
    :returns: Owner name
    '''
    file_stat = stat(file_name)
    try:
        owner = pwd.getpwuid(file_stat.st_uid).pw_name
    except KeyError:
        owner = "None"
    return owner

def main():
    '''
    Main entry point function
    '''
    if "postgres" != get_owner(POSTGRES_CONFIG):
        call(["chown", "-R", "postgres", POSTGRES_CONFIG])

    if "postgres" != get_owner(POSTGRES_PATH):
        call(["chown", "-R", "postgres", POSTGRES_PATH])

    if listdir(POSTGRES_PATH) == []:
        call(['pg_createcluster', '9.3', 'main', '-e=utf8'])
        with open(path.join(POSTGRES_CONFIG, "9.3", "main", "pg_hba.conf"), "a") as pg_hba:
            pg_hba.write("host all  all    0.0.0.0/0  md5")
        with open(path.join(POSTGRES_CONFIG, "9.3", "main", "postgresql.conf"), "a") as pg_config:
            pg_config.write("listen_addresses='*'")
        call(["/etc/init.d/postgresql", "start"])
        call(["su", "postgres", "-c /config_db.py"])
        call(["/etc/init.d/postgresql", "stop"])
    call(["/usr/bin/supervisord"])

if __name__ == '__main__':
    main()
