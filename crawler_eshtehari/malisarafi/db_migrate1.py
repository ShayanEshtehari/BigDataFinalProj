from db_malisarafi import Page, News, pg_db
import html
import urllib.parse
from playhouse.postgres_ext import *
from settings import PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_POSTGRES_PASSWORD
import playhouse.postgres_ext as pwe

pg_db = PostgresqlExtDatabase('postgres', user='postgres', password=PG_POSTGRES_PASSWORD,
                           host=PG_HOST, port=PG_PORT) # , autorollback=True

# exception raises again in except
# pg_db.connect()
# for row in Page.select():
#     try:
#         row.url = urllib.parse.unquote(row.url)
#         row.save()
#         print(f'\rsaved {row.id}       ', end='')
#     except pwe.IntegrityError:
#         row.delete_instance()
#         print(f'\rDELETED {row.id}       ', end='')
# pg_db.close()


# same issue
# with pg_db.atomic():
#     for row in Page.select():
#         try:
#             row.url = urllib.parse.unquote(row.url)
#             row.save()
#             pg_db.commit()
#             print(f'\rsaved {row.id}       ', end='')
#         except pwe.IntegrityError:
#             pg_db.rollback()
#             row.delete_instance()
#             print(f'\rDELETED {row.id}       ', end='')



# psycopg2.errors.InFailedSqlTransaction
# def f(model_instance, column_name):
#     try:
#         with pg_db.atomic():
#             model_instance = Page.get(id=model_instance.id)
#             setattr(model_instance, column_name, urllib.parse.unquote(getattr(model_instance, column_name)))
#             model_instance.save()
#     except pwe.IntegrityError:
#         pass
# pg_db.connect()
# for row in Page.select():
#     f(row, 'url')
# pg_db.close()


pg_db.connect()
for row in Page.select():
    new_url = urllib.parse.unquote(row.url)
    existing_row = Page.select().where(Page.url == new_url).first()
    if existing_row and existing_row.id != row.id:
        try:
            row.delete_instance(recursive=True, delete_nullable=False)
        except: # foreign key
            pwe.IntegrityError
        print(f'\rDELETED {row.id}       ', end='')
    else:
        row.url = new_url
        row.save()
        print(f'\rsaved {row.id}       ', end='')
pg_db.close()

