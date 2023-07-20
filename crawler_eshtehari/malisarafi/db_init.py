from playhouse.postgres_ext import *
from settings import PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_POSTGRES_PASSWORD

pg_db = PostgresqlExtDatabase('postgres', user='postgres', password=PG_POSTGRES_PASSWORD,
                           host=PG_HOST, port=PG_PORT) # , autorollback=True


# sql1 = "CREATE USER %s WITH PASSWORD '%s';" % (PG_USER, PG_PASSWORD)
sql1 = f"""
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = '{PG_USER}') THEN

      RAISE NOTICE 'Role "{PG_USER}" already exists. Skipping.';
   ELSE
      BEGIN   -- nested block
         CREATE ROLE {PG_USER} LOGIN PASSWORD '{PG_PASSWORD}';
      EXCEPTION
         WHEN duplicate_object THEN
            RAISE NOTICE 'Role "{PG_USER}" was just created by a concurrent transaction. Skipping.';
      END;
   END IF;
END
$do$;
"""
esql1 = pg_db.execute_sql(sql1)

# sql2 = "CREATE DATABASE %s WITH ENCODING 'UTF8' OWNER %s;" % (PG_DATABASE, PG_USER)
sql2 = f"""
DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = '{PG_DATABASE}') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      -- PERFORM dblink_exec('dbname=' || current_database()  -- current db
      --                  , 'CREATE DATABASE {PG_DATABASE}');
      BEGIN   -- nested block
      CREATE DATABASE {PG_DATABASE} WITH ENCODING 'UTF8' OWNER {PG_USER};
      EXCEPTION
         WHEN duplicate_object THEN
            RAISE NOTICE 'Database "{PG_DATABASE}" was just created by a concurrent transaction. Skipping.';
      END;
   END IF;
END
$do$;
"""
# peewee.InternalError: CREATE DATABASE cannot run inside a transaction block
# esql2 = pg_db.execute_sql(sql2)
# sqlalchemy.exc.InternalError: (psycopg2.errors.ActiveSqlTransaction) CREATE DATABASE cannot run inside a transaction block
# from sqlalchemy import create_engine
url = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
conn_url = f"postgresql://postgres:{PG_POSTGRES_PASSWORD}@{PG_HOST}:{PG_PORT}/postgres"
# engine = create_engine(conn_url)
# with engine.connect() as conn:
#     conn.execute(sql2)
# from sqlalchemy_utils import database_exists, create_database
# if not database_exists(url):
#     create_database(url)
# sqlalchemy.exc.ProgrammingError: (psycopg2.errors.InsufficientPrivilege) permission denied to create database
# print(database_exists(url))
# conn = engine.raw_connection()
# conn.autocommit = False
# conn.cursor().execute(sql2)

# from django.db import connection
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': PG_DATABASE,
#         'USER': PG_USER,
#         'PASSWORD': PG_PASSWORD,
#         'HOST': PG_HOST,
#         'PORT': PG_PORT,
#     },
# }
# with connection.cursor() as cursor:
#     cursor.execute(sql2)
# django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.

import psycopg2
conn = psycopg2.connect(
    host = PG_HOST,
    user = 'postgres',
    password = PG_POSTGRES_PASSWORD,
    port = PG_PORT,
    dbname = 'postgres',
)
# conn.set_session(isolation_level='autocommit')
conn.autocommit = True 
conn.cursor().execute(sql2)
conn.close()

from db_malisarafi import Page, News, pg_db

# with pg_db:
#     pg_db.drop_tables([Page, News])

with pg_db:
    pg_db.create_tables([Page, News])

sql3 = "INSERT INTO page (url, status) values('https://www.tgju.org/news', 'TODO');"
esql3 = pg_db.execute_sql(sql3)
# print(esql3.fetchall()) # psycopg2.ProgrammingError: no results to fetch
