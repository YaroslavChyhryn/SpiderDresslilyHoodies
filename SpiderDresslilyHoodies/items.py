import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re
from datetime import datetime


def product_id_from_product_url(url):
    return int(re.search('product(\d+)', url).group(1))


def format_product_info(product_info):
    product_info = re.findall(r'<strong>(.*?)((?:<br>|\n))', product_info)
    product_info = [info_pair.replace('</strong> ', '').rstrip() for info_pair, appendix in product_info]
    product_info = ';'.join(product_info)
    return product_info


def string_to_int(price):
    try:
        return int(price)
    except ValueError:
        return []

def string_to_float(price):
    try:
        return float(price)
    except ValueError:
        return []

def check_display_attr(element):
    if re.search(r'inline-block', element):
        return re.findall(r'data-orgp="(.*?)"', element)
    else:
        return []

def url_from_splash_url(url):
    return re.findall(r'url=(.*?)(&time)', url)


def count_rating(stars):
    return stars.count('icon-star-black')


def format_color(color):
    try:
        color = re.findall(r'Color: (.*?)(<)', color)[0]
        return color
    except IndexError:
        return []

def format_size(size):
    try:
        size = re.findall(r'Size: (.*?)(<)', size)[0]
        return size
    except IndexError:
        return []

def format_time(time):
    datetime_obj = datetime.strptime(time, '%b,%d %Y %H:%M:%S')
    return datetime_obj.timestamp()


class SpiderdresslilyHoodiesItem(scrapy.Item):
    product_id = scrapy.Field(input_processor=(MapCompose(product_id_from_product_url)),
                              output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=(MapCompose(remove_tags)),
                        output_processor=TakeFirst())
    discount = scrapy.Field(input_processor=(MapCompose(remove_tags,
                                                        string_to_int)),
                            output_processor=TakeFirst())
    discounted_price = scrapy.Field(input_processor=(MapCompose(string_to_float)),
                                    output_processor=TakeFirst())
    original_price = scrapy.Field(input_processor=(MapCompose(string_to_float)),
                                  output_processor=TakeFirst())
    total_reviews = scrapy.Field(input_processor=(MapCompose(remove_tags,
                                                             string_to_int)),
                                 output_processor=TakeFirst())
    product_info = scrapy.Field(input_processor=(MapCompose(format_product_info)),
                                output_processor=TakeFirst())


class SpiderdresslilyReviewsItem(scrapy.Item):
    product_id = scrapy.Field(input_processor=(MapCompose(product_id_from_product_url)),
                              output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=(MapCompose(count_rating)),
                          output_processor=TakeFirst())
    timestamp = scrapy.Field(input_processor=(MapCompose(remove_tags, format_time)),
                             output_processor=TakeFirst())
    text = scrapy.Field(input_processor=(MapCompose(remove_tags)),
                        output_processor=TakeFirst())
    size = scrapy.Field(input_processor=(MapCompose(format_size)),
                        output_processor=TakeFirst())
    color = scrapy.Field(input_processor=(MapCompose(format_color)),
                         output_processor=TakeFirst())

