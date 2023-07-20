# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MalisarafiItem(scrapy.Item):
    id = scrapy.Field()
    page_id = scrapy.Field()
    url = scrapy.Field()
    head = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
    text = scrapy.Field()
    summary = scrapy.Field()
  