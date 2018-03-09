# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # book_url = scrapy.Field()
    img_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    kind = scrapy.Field()
    update_status = scrapy.Field()
    word_num = scrapy.Field()
    brief = scrapy.Field()



