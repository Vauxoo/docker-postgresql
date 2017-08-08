#!/usr/bin/python

import psycopg2

try:
    conn = psycopg2.connect("dbname='template1'")
    conn.set_isolation_level(0)
except:
    print "Could not connect to PostgreSQL server"
    raise

cursor = conn.cursor()

try:
    print "Activate unnacent etension for all databases by defult"
    cursor.execute("CREATE EXTENSION \"unaccent\";")
except:
    print "Could not create extension"
    raise

try:
    print "Creating users"
    cursor.execute("CREATE USER docker WITH SUPERUSER PASSWORD 'docker';")
    cursor.execute("CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';")
except:
    print "Could not create users"
    raise

try:
    print "Creating docker database"
    cursor.execute("CREATE DATABASE docker ENCODING 'utf8' OWNER docker TEMPLATE template1 ")
except:
    print "Could not create docker database"
    raise

cursor.close()
conn.close()
