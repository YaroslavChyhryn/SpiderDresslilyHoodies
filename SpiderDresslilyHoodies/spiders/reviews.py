import scrapy
from scrapy import Selector
from SpiderDresslilyHoodies.items import SpiderdresslilyReviewsItem
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['dresslily.com']
    start_urls = ['https://www.dresslily.com/hoodies-c-181.html']
    base_url = 'https://www.dresslily.com'

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        # todo сначало отсортировать по количеству отзывов, это значитено ускорит процесс краулинга
        hoodie_page_links = response.css('a.goods-name-link::attr(href)').getall()

        for url in hoodie_page_links:
            self.driver.get(url)
            next_page = True
            while next_page:
                time.sleep(1)
                html = self.driver.page_source
                response_obj = Selector(text=html)
                reviews = response_obj.css('div.reviewinfo')
                next_page = response_obj.xpath(
                    "//a[@class=' site-pager-next' and @class!='site-pager-disabled']").extract()

                for review in reviews:
                    l = ItemLoader(item=SpiderdresslilyReviewsItem(), selector=review)

                    l.add_value('product_id', self.driver.current_url)
                    l.add_css('timestamp', 'span.review-time')
                    l.add_css('rating', 'span.review-star')
                    l.add_css('text', 'div.review-content-text')
                    l.add_css('size', 'div.review-good-size-box-pc')
                    l.add_css('color', 'div.review-good-size-box-pc')

                    yield l.load_item()

                # selenium.common.exceptions.NoSuchElementException:
                try:
                    next_page = self.driver.find_element_by_xpath(
                        "//a[@class=' site-pager-next' and @class!='site-pager-disabled']")
                    self.driver.execute_script("arguments[0].click();", next_page)
                except NoSuchElementException:
                    next_page = False
                    break

        next_page_partial_url = response.css('li.next-page a').attrib['href']
        if next_page_partial_url is not None:
            next_page_url = self.base_url + next_page_partial_url
            yield scrapy.Request(next_page_url, callback=self.parse)
