import scrapy
import urllib.parse
import scrapy.exceptions
import random
from ..db_malisarafi import Page, News, pg_db
from ..items import MalisarafiItem
import playhouse.postgres_ext as pwe
import logging
import html
import re


class BasicSpider(scrapy.Spider):
    name = 'crawl'
    allowed_domains = [ # Does not work when manual db mgmt
        'tgju.org',
        # 'ramzarz.news',
        # 'tejaratnews.com',
    ]
    # start_urls = ['https://www.tgju.org',
    #               'https://ramzarz.news',
    #               'https://tejaratnews.com',
    # ]
    start_urls = [
        'https://www.tgju.org/news',
    ]


    @property
    def proxy(self):
        return self.settings.get('PROXY')


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        logging.getLogger('peewee').setLevel(logging.INFO)

        from_crawler = super(BasicSpider, cls).from_crawler
        spider = from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.idle, signal=scrapy.signals.spider_idle)

        # Settings initialization
        settings = scrapy.utils.project.get_project_settings() # cls.settings is not available

        # User agents
        ua = settings.get('USER_AGENTS')
        ual = []
        with open(ua) as fd:
            for line in fd.readlines():
                line = line.strip()
                if line.startswith('#'):
                    continue
                ual.append(line)
            fd.close()
        cls.user_agent_list = ual

        return spider


    def next_url(self):
        # SELECT count(*) FROM news WHERE url ~ 'https://www\.tgju\.org/news/\d+/[\u0600-\u06FF]+';
        # search_pattern = r'https://www\.tgju\.org/news/\d+/[\u0600-\u06FF]+'
        while True:
            # query = Page.select(Page.id, Page.url).where((Page.status == 'TODO') & (Page.url.iregexp(search_pattern))).order_by(pwe.fn.Random()).first()
            query = Page.select(Page.id, Page.url).where((Page.status == 'TODO')).order_by(pwe.fn.Random()).first()
            if query:
                page_id = query.id
                url = query.url
                update_query = Page.update(status='PENDING').where(Page.id == page_id)
                exec_query = update_query.execute()
                if exec_query == 0:
                    self.logger.info('Query did not update to pending on id: %s, url: %s , querying next url.', page_id, url)
                    continue
                else:
                    return page_id, url
            else:
                return None


    def idle(self):
        # test proxy
        # raise scrapy.exceptions.CloseSpider('Test finished')
    
        self.logger.info('Querying next url.')
        query = self.next_url()
        if query:
            page_id, url = query
            user_agent = random.choice(self.user_agent_list)
            self.crawler.engine.crawl(scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'proxy': self.proxy, 'dont_merge_cookies': True}, cb_kwargs={'page_id': page_id}, headers={'user-agent': user_agent}))
        else:
            self.logger.info('No more queries to run.')


    def start_requests(self):
        # test proxy
        # user_agent = random.choice(self.user_agent_list)
        # yield scrapy.Request('http://icanhazip.com', callback=self.test_proxy, dont_filter=True, meta={'proxy': self.proxy, 'dont_merge_cookies': True}, headers={'user-agent': user_agent})
        # return
    
        self.logger.info('Starting requests!')
        # query = self.next_url()
        # if query:
        #     page_id, url = query
        #     user_agent = random.choice(self.user_agent_list)
        #     yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'proxy': self.proxy, 'dont_merge_cookies': True}, cb_kwargs={'page_id': page_id}, headers={'user-agent': user_agent})
        # else:
        #     self.logger.info('No more queries to run.')
        for url in self.start_urls:
            page_id = -1
            user_agent = random.choice(self.user_agent_list)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'proxy': self.proxy, 'dont_merge_cookies': True}, cb_kwargs={'page_id': page_id}, headers={'user-agent': user_agent})
        else:
            self.logger.info('No more queries to run.')
    

    def test_proxy(self, response):
        # test proxy
        self.logger.info('Parsing url %s', response.url)
        self.logger.info('IP: %s', response.body)
        raise scrapy.exceptions.CloseSpider('Test finished')


    def parse_news_tgju(self, response):
        try:
            head = response.css('#news-main > div > div.news-container h1.news-article-title.font-title-24.single-title a::text').get().strip()
        except:
            head = ''

        try:
            author = response.css("a[href*='/news/writer/']::text").get().strip()
        except:
            author = ''

        try:
            category = response.css('#news-main > div > div.news-container a.news-article-tag.outline-tag::text').get().strip()
        except:
            category = ''

        try:
            date = response.css('#news-main > div > div.news-container div.article-time::text').get().strip()
            date = re.sub(' ساعت .*', '', date).strip()
        except:
            date = ''

        try:
            tags_texts = response.css('#news-main > div > div.news-container ul.news-article-tags *::text').getall()
            tags_texts = [re.sub('\n', '', t).strip() for t in tags_texts]
            tags = '|'.join([el for el in tags_texts if el.strip()])
        except:
            tags = ''

        try:
            text_texts = response.css('#news-main > div > div.news-container div.news-article-single-content *::text').getall()
            text = ''
            for t in text_texts:
                t = re.sub('\n', '', t).strip()
                if t:
                    t = html.unescape(t)
                    text += t
        except:
            text = ''

        try:
            summary_texts = response.css('#news-main > div > div.news-container div.summary *::text').getall()
            summary = ''
            for t in summary_texts:
                t = re.sub('\n', '', t).strip()
                if t:
                    t = html.unescape(t)
                    summary += t
        except:
            summary = ''

        d = dict(head=head, author=author, category=category, date=date, tags=tags, text=text, summary=summary)
        return d


    def parse(self, response, page_id):
        response_url = urllib.parse.unquote(response.url)
        self.logger.info('Parsing url %s', response_url)
        database = pg_db

        # scrape data
        with database.atomic():
            if 'tgju.org/news/' in response_url:
                d = self.parse_news_tgju(response)
                i = MalisarafiItem(**d)
                try:
                    create = News.create(
                        page_id = page_id,
                        url = response_url,
                        **d
                    )
                    database.commit()
                    create_id = create.id
                    self.logger.info('Inserted new news %s in the database with id %s!', response_url, create_id)
                    yield i
                except pwe.IntegrityError:
                    self.logger.info('Url %s already exists in the database!', response_url)
                    database.rollback()
                    create_id = None

        # find new links
        with database.atomic():
            for anchor in response.css('a'):
                if 'href' in anchor.attrib:
                    url = anchor.attrib['href']
                    joined_url = urllib.parse.urljoin(response_url, urllib.parse.unquote(url))
                    if '://' in joined_url: # Passing javascript:showf() urls # doesn't pass mailto:...http://..
                        parsed_url = urllib.parse.urlparse(joined_url)
                        # if 'tgju.org' in joined_url:
                        # if (parsed_url.netloc == 'tgju.org') and ('tgju.org/news' in joined_url): # doesn't work
                        if 'tgju.org/news' in joined_url:
                            domain = joined_url
                            index_of_slash = domain.find('/')
                            if index_of_slash != -1:
                                domain = domain[:index_of_slash]
                            pattern = rf'^((.*\.)+)?({"|".join(self.allowed_domains)})$'
                            if re.match(pattern, domain):
                                try:
                                    create = Page.create(
                                        url = joined_url,
                                        status = 'TODO'
                                    )
                                    database.commit()
                                    create_id = create.id
                                    self.logger.info('Inserted new url %s in the database with id %s!', joined_url, create_id)
                                except pwe.IntegrityError:
                                    database.rollback()
                                    create_id = None
                                    # self.logger.info('Url %s already exists in the database!', joined_url)

        if page_id != -1:
            q = Page.update(status = 'DONE').where(Page.id == page_id)
            e = q.execute()
            if e == 0:
                self.logger.warning('Could not update page with id %s, url %s to DONE.', page_id, response_url)
