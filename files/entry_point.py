#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir, stat, chown, path
from subprocess import call
import fileinput
import pwd
import re

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
        call(["chown", "-R", "postgres:postgres", POSTGRES_CONFIG])
        call(["chmod", "-R", "0700", POSTGRES_CONFIG])

    if "postgres" != get_owner(POSTGRES_PATH):
        call(["chown", "-R", "postgres:postgres", POSTGRES_PATH])
        call(["chmod", "-R", "0700", POSTGRES_PATH])

    if listdir(POSTGRES_PATH) == []:
        call(['pg_createcluster', '9.5', 'main', '-e=utf8'])
        with open(path.join(POSTGRES_CONFIG, "9.5", "main", "pg_hba.conf"), "a") as pg_hba:
            pg_hba.write("host all  all    0.0.0.0/0  md5")
        for line in fileinput.input(path.join(POSTGRES_CONFIG, "9.5", "main", "postgresql.conf"), inplace=True):
            line = re.sub(r'#?(listen_addresses) .*$', r"\1 = '*'", line.strip())
            line = re.sub(r'#?(temp_buffers) .*$', r"\1 = 16MB", line.strip())
            line = re.sub(r'#?(work_mem) .*$', r"\1 = 16MB", line.strip())
            line = re.sub(r'#?(max_stack_depth) .*$', r"\1 = 7680kB", line.strip())
            print(line)
        call(["/etc/init.d/postgresql", "start"])
        call(["su", "postgres", "-c /config_db.py"])
        call(["/etc/init.d/postgresql", "stop"])
    call(["/usr/bin/supervisord"])

if __name__ == '__main__':
    main()
