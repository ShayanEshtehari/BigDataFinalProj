from playhouse.postgres_ext import *
try:
    from .settings import PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT # scrapy
except:
    from settings import PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT # standalone module
pg_db = PostgresqlExtDatabase(PG_DATABASE, user=PG_USER, password=PG_PASSWORD,
                           host=PG_HOST, port=PG_PORT) # , autorollback=True


class BaseModel(Model):
    class Meta:
        database = pg_db


class Page(BaseModel):
    id = AutoField()
    url = CharField(max_length=2048, unique=True)
    status = CharField(max_length=50)


class News(BaseModel):
    id = AutoField()
    page_id = ForeignKeyField(Page, null=True)
    url = CharField(max_length=2048, unique=True)
    head = CharField(max_length=100)
    author = CharField(max_length=100)
    category = CharField(max_length=50)
    date = CharField(max_length=50)
    tags = TextField()
    text = TextField()
    summary = TextField()
