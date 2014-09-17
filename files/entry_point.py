#!/usr/bin/python

from  os import listdir
from subprocess import Popen, call

postgres_path = '/var/lib/postgresql' 
if listdir(postgres_path) == []: 
    call(['pg_createcluster', '9.3', 'main', '-e=utf8'])
    with open("/etc/postgresql/9.3/main/pg_hba.conf", "a") as pg_hba:
        pg_hba.write("host all  all    0.0.0.0/0  md5")
    with open("/etc/postgresql/9.3/main/postgresql.conf", "a") as pg_config:
        pg_config.write("listen_addresses='*'")
    call(["/etc/init.d/postgresql", "start"])
    call(["su", "postgres", "-c /config_db.py"])
    call(["/etc/init.d/postgresql", "stop"])
Popen("/usr/bin/supervisord").pid
