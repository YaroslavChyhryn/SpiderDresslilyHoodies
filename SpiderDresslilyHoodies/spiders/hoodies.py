import scrapy
from scrapy_splash import SplashRequest
from SpiderDresslilyHoodies.items import SpiderdresslilyHoodiesItem
from scrapy.loader import ItemLoader


class HoodieSpider(scrapy.Spider):
    name = 'hoodie'
    allowed_domains = ['dresslily.com']
    start_urls = ['https://www.dresslily.com/hoodies-c-181.html']
    base_url = 'https://www.dresslily.com'

    def parse(self, response):
        hoodie_page_links = response.css('a.goods-name-link::attr(href)').getall()

        for url in hoodie_page_links:
            yield SplashRequest(url, self.parse_hoodie, args={'timeout': 10, 'wait': 5})

        next_page_partial_url = response.css('li.next-page a').attrib['href']
        if next_page_partial_url is not None:
            next_page_url = self.base_url + next_page_partial_url
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_hoodie(self, response):
        l = ItemLoader(item=SpiderdresslilyHoodiesItem(), response=response)

        l.add_value('product_id', response.url)
        l.add_value('product_url', response.url)
        l.add_css('name', 'span.goodtitle')
        l.add_xpath('discount', '//span[@class="off js-dl-cutoff"]/span')
        l.add_css('original_price', 'span.curPrice::attr(data-orgp)')
        l.add_css('discounted_price', 'span.js-dl-marketPrice')
        l.add_css('total_reviews', 'strong#js_reviewCountText')

        l.add_xpath('product_info', '//div[@class="xxkkk20"]')

        yield l.load_item()
