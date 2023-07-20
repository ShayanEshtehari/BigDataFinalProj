from django.contrib import admin

# Register your models here.
# from .models import Post
from .models import * # new

from import_export.admin import ExportActionMixin # new

from django.contrib.auth.admin import UserAdmin # new

class Export(ExportActionMixin, admin.ModelAdmin): # new
    # list_display = ('title', 'author', 'body')
    pass

admin.site.register(NewsModel, Export)
