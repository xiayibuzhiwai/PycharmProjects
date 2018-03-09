# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from scrapy.http import Request
from ..items import NovelItem


class ReadnovelSpider(scrapy.Spider):
    name = 'readnovel'
    allowed_domains = ['readnovel.com']
    start_urls = ['https://www.readnovel.com/free/all']
    book_dict = {}

    def parse(self, response):
        html = Selector(response)
        book_items = html.xpath("//div[@class='right-book-list']//li")

        for item in book_items:
            introduction_url = item.xpath("./div[@class='book-img']/a/@href").extract_first()       # 书籍地址：/book/8410348603558103
            img_url = item.xpath("./div[@class='book-img']//img/@src").extract_first()      # 图片地址
            title = item.xpath("./div[@class='book-info']/h3/a/@title").extract_first()     # 标题
            author = item.xpath("./div[@class='book-info']/h4/a/text()").extract_first()    # 作者
            tag = item.xpath("./div[@class='book-info']/p[@class='tag']")
            kind = tag.xpath("./span[@class='org']/text()").extract_first()                 # 书籍类型：如 武侠
            update_status = tag.xpath("./span[@class='red']/text()").extract_first()        # 更新状态：如 完结、连载
            word_num = tag.xpath("./span[@class='blue']/text()").extract_first()            # 书籍字数
            brief = item.xpath("./div[@class='book-info']/p[@class='intro']").extract_first()   # 书籍简介
            book = {"book_url": "https://www.readnovel.com"+introduction_url,
                    "img_url": img_url,
                    "title": title,
                    "author": author,
                    "kind": kind,
                    "update_status": update_status,
                    "word_num": word_num,
                    "brief": brief
                    }
            self.book_dict.setdefault(introduction_url, book)
            # item = NovelItem(**book)
            # yield item

            # yield NovelItem(
            #     # book_url=book_url,
            #     img_url=img_url,
            #     title=title,
            #     author=author,
            #     kind=kind,
            #     update_status=update_status,
            #     word_num=word_num,
            #     brief=brief
            # )

            yield Request(
                url="https://www.readnovel.com"+introduction_url,
                meta={"book": book},
                callback=self.get_content_url
            )
        # print(self.book_dict)

        base_page_url = "https://www.readnovel.com/free/all?pageNum={0}&pageSize=10&gender=2&catId=-1&isFinish=-1&isVip=1&size=-1&updT=-1&orderBy=0"
        # page_list = html.xpath("//div[@id='page-container']//a[@class='lbf-pagination-page  ']/@data-page").extract()
        # print(page_list)
        # for page in page_list:

        # for page in range(1, 10):     # range(1, 4771)
        #     page_url = base_page_url.format(page)
        #     yield Request(
        #         url=page_url,
        #         callback=self.parse
        #     )

    def get_content_url(self, response):
        html = Selector(response)
        # content_url = html.xpath("//div[@class='chapter-control']/a[@target='_blank']/@href").extract_first()
        content_url = html.xpath("//a[@id='readBtn']/@href").extract_first()
        book = response.meta['book']
        print(content_url)
        print(b'\xe7'.decode("utf-8"))
        yield Request(
            url="https:"+content_url,
            meta={"book": book},
            headers={"Referer": book["book_url"],
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
                     "Upgrade-Insecure-Requests": 1},
            cookies={"_csrfToken": "a2dhB9hLfgqEDHVpUxgvJ2DnCDQ74WPZMyxqfuCF",
                    "newstatisticUUID": "1509590050_1901143994",
                    "qdrs":"0%7C3%7C0%7C0%7C1",
                    "qdgd":1},
            callback=self.get_content
        )

    def get_content(self, response):
        print("===========================")
        # print(response.url)
        # html = Selector(response)
        # ctime = html.xpath("//div[@class='info-list cf']/ul/li/em/text()").extract_first()
        # directory_url = html.xpath("//div[@class='chapter-control']/a[@target='_blank']/@href").extract_first()
        # print(ctime)
        # print()
        # print(directory_url)


