# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
import hashlib
import mimetypes
import os
from itemadapter import ItemAdapter
from scrapy.utils.python import to_bytes
import urllib.parse
import re
import scrapy
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings


class MalisarafiPipeline:
    def process_item(self, item, spider):
        return item

class MalisarafiFilesPipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.proxy = settings.get('PROXY')
        super().__init__(store_uri, download_func=download_func, settings=settings)


    def get_media_requests(self, item, info):
        meta = {'proxy': self.proxy}
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        return [scrapy.Request(u, cookies=item.get('cookies'), meta=meta) for u in urls]


    def file_path(self, request, response=None, info=None, *, item=None):
        media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        media_ext = os.path.splitext(request.url)[1]
        if media_ext not in mimetypes.types_map:
            media_ext = ''
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return f'{media_guid}{media_ext}'
