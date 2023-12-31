# Scrapy settings for malisarafi project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import copy

from colorlog import ColoredFormatter
import scrapy.utils.log

color_formatter = ColoredFormatter(
    (
        '%(log_color)s%(levelname)-5s%(reset)s '
        '%(yellow)s[%(asctime)s]%(reset)s'
        '%(white)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'
    ),
    datefmt='%y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold_cyan',
        'WARNING': 'red',
        'ERROR': 'bg_bold_red',
        'CRITICAL': 'red,bg_white',
    }
)

_get_handler = copy.copy(scrapy.utils.log._get_handler)

def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler

scrapy.utils.log._get_handler = _get_handler_custom

import logging
# logging.getLogger('peewee').setLevel(logging.INFO)

BOT_NAME = 'malisarafi'

SPIDER_MODULES = ['malisarafi.spiders']
NEWSPIDER_MODULE = 'malisarafi.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'malisarafi.middlewares.MalisarafiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'malisarafi.middlewares.MalisarafiDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'malisarafi.pipelines.MalisarafiPipeline': 300,
    # 'scrapy.pipelines.files.FilesPipeline':1
    'malisarafi.pipelines.MalisarafiFilesPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Custom settings
FEED_EXPORT_ENCODING = 'utf-8'
DNSCACHE_ENABLED = False 
# HTTPPROXY_ENABLED = True # Default is True
RETRY_TIMES = 10
RETRY_HTTP_CODES = list(set([500, 502, 503, 504, 522, 524, 408, 429] + [500, 503, 504, 400, 403, 408]))
TELNETCONSOLE_PASSWORD = "2jx6L%U2m0nV"
# DUPEFILTER_DEBUG = True

# Spider settings
RETRY_COUNT = 5
PDF_DOWNLOAD_TIMEOUT = 1000

PG_DATABASE = 'malisarafi'
PG_USER = 'malisarafiuser'
PG_PASSWORD = 'chJ1L^nokFvga8'
PG_HOST = '127.0.0.1'
PG_PORT = 5432
PG_POSTGRES_PASSWORD = 'JB3GvuzOpgV2'

# Paths
import os, pathlib, scrapy.utils.project
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(scrapy.utils.project.closest_scrapy_cfg()))) # /home/shayan/malisarafi # , os.path.pardir
USER_AGENTS = os.path.abspath(os.path.join(PROJECT_DIR, 'user_agents.txt'))
DOWNLOAD_PATH = os.path.abspath(os.path.join(PROJECT_DIR, 'Downloads')) # '/root/malisarafi/Downloads/'

PROXY = '' # set this to not use proxy
# PROXY = 'http://127.0.0.1:10809'
# PROXY = 'http://127.0.0.1:21204'
