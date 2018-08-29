BOT_NAME = 'Scrapy_GoogleSearch'

SPIDER_MODULES = ['Scrapy_GoogleSearch.spiders']
NEWSPIDER_MODULE = 'Scrapy_GoogleSearch.spiders'


ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {'scrapy_crawlera.CrawleraMiddleware': 300}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '******'

