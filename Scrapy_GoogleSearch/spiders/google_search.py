import scrapy
import re
from urllib.parse import urljoin
from Scrapy_GoogleSearch.items import ScrapyGooglesearchItem


class GoogleSearch(scrapy.Spider):
    name = 'google_crawler'
    allowed_domains = ['google.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36',
    }

    def __init__(self, url=None, *args, **kwargs):
        super(GoogleSearch, self).__init__(*args, **kwargs)
        self.count = 0
        self.start_urls = [url]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=self.headers)

    def parse(self, response):
        item = ScrapyGooglesearchItem()

        selector_array = response.xpath('//div[@class="g"]//div[@class="rc"]')
        if self.count == 22:
            selector_array = selector_array[:5]

        for selector in selector_array:
            text = selector.xpath('./h3/a/text()').extract()
            name = re.search('(.*?) -', text[0], re.DOTALL)
            item['name'] = name.group(1) if name else None
            item['title'] = text[0] if text else None
            link = selector.xpath('./h3/a/@href').extract()
            item['link'] = link[0] if link else None
            if '-' in text[0]:
                item['role'] = text[0].split('-')[1].strip()
            desc = selector.xpath('./div[@class="s"]//span[@class="st"]//text()').extract()
            item['description'] = ''.join(desc).replace(';', ',') if desc else None

            yield item

        if self.count < 22:
            next_link = response.xpath('//a[@id="pnnext"]/@href').extract()
            if next_link:
                next_link = urljoin(response.url, next_link[0])
                self.count += 1
                yield scrapy.Request(url=next_link, headers=self.headers, callback=self.parse)