#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("dbname='postgres'")
conn.set_isolation_level(0)
cursor = conn.cursor()
cursor.execute("CREATE USER docker WITH SUPERUSER PASSWORD 'docker';")
cursor.execute("CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';")
cursor.execute("CREATE DATABASE docker ENCODING 'utf8' OWNER docker TEMPLATE template1 ")
conn.commit()
cursor.close()
conn.close()
