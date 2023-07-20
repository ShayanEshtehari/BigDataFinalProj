from django.db import models
from django.urls import reverse

# from django.contrib.auth.models import User # new
from django.contrib.auth.models import AbstractUser # new
from django.utils.translation import gettext_lazy as _ # new
from django.contrib.auth.hashers import make_password # new

# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class NewsModel(DjangoCassandraModel):
    id       = columns.UUID(primary_key=True, default=uuid.uuid4)
    url      = columns.Text()
    head     = columns.Text()
    author   = columns.Text()
    category = columns.Text()
    date     = columns.Text()
    tags     = columns.Text()
    text     = columns.Text()
    summary  = columns.Text()
    hashtags  = columns.Text()
    keywords  = columns.Text()
