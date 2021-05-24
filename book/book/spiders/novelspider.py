import scrapy
from scrapy_redis.spiders import RedisSpider
import requests
from copy import deepcopy
import re


class NovelSpider(RedisSpider):
    name = 'novelspider'
    # start_urls = ['https://www.qb5.tw/']
    redis_key = 'nov'

    def parse(self, response):
        category_list = response.xpath('//div[@class="nav_cont"]/ul/li')[1:-2]
        for category in category_list:
            item = {}
            category_name = category.xpath('./a/text()').extract_first()
            category_url = category.xpath('./a/@href').extract_first()
            item["category_name"] = category_name
            yield scrapy.Request(category_url, meta={"item": item}, callback=self.get_book)

    def get_book(self, response):
        item = response.meta["item"]
        book_list = response.xpath('//div[@class="zp"]')
        for book in book_list:
            book_name = book.css('./a/text()').extract_first()
            book_url = book.css('./a/@href').extract_first()
            item["book_name"] = book_name
            yield scrapy.Request(book_url, meta={"item": item}, callback=self.get_chapter)
        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.get_book, meta={'item': deepcopy(item)})

    def get_chapter(self, response):
        item = response.meta["item"]
        author = response.xpath('//small/a/text()').extract_first()
        intro = ''.join(response.css('#intro').xpath('.//text()').extract()).strip().replace('\xa0', '')
        image_url = response.css('.img_in img::attr(src)').extract_first()

        image = requests.get(url=image_url).content
        file_name = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['book_name'], re.S))
        with open('images/{}.jpg'.format(file_name), 'wb') as f:
            f.write(image)

        image = 'images/{}.jpg'.format(file_name)

        chapter_list = response.css('dd a')
        number = 0
        for chapter in chapter_list:
            number += 1
            chapter_name = chapter.css('a::text').extract_first()
            chapter_url = chapter.css('a::attr(href)').extract_first()
            chapter_url = response.url + chapter_url
            item['author']: author
            item['intro']: intro
            item['image']: image
            item['chapter_name']: chapter_name
            item['number']: number

            yield scrapy.Request(chapter_url, meta={"item": item}, callback=self.get_content)

    def get_content(self, response):
        item = response.meta["item"]
        content = ''.join(re.findall('</a>最新章节！(.*)</div><center class="clear">', response.text, re.S))
        item['content']: content
        yield item
