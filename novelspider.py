import scrapy
from scrapy_redis.spiders import RedisSpider
import requests
from ..items import NovelSpiderItem
from copy import deepcopy
import re


class NovelSpider(RedisSpider):
    name = 'novelspider'
    start_urls = ['https://www.qb5.tw/']
    redis_key = 'nov'

    def parse(self, response):
        category_list = response.xpath('//div[@class="nav_cont"]/ul/li')[1:-2]
        for category in category_list:
            category_name = category.css('a::text').extract()[0]
            category_url = category.css('a::attr(href)').extract()[0]
            meta = {
                'category_name': category_name
            }
            yield scrapy.Request(category_url, meta=meta, callback=self.get_book)

    def get_book(self, response):
        meta = response.meta
        book_list = response.xpath('//div[@class="zp"]')
        for book in book_list:
            book_name = book.css('a::text').extract()[0]
            book_url = book.css('a::attr(href)').extract()[0]
            meta.update({
                'book_name': book_name
            })
            yield scrapy.Request(book_url, meta=meta, callback=self.get_chapter)
        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.get_book, meta=deepcopy(meta))

    def get_chapter(self, response):
        meta = response.meta
        author = response.xpath('//small/a/text()').extract_first()
        intro = ''.join(response.css('#intro').xpath('.//text()').extract()).strip().replace('\xa0', '')
        image_url = response.css('.img_in img::attr(src)').extract()[0]

        image = requests.get(url=image_url).content
        file_name = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', meta['book_name'], re.S))
        with open('D:/XS/novel_site/static/images/{}.jpg'.format(file_name), 'wb') as f:
            f.write(image)
        print(meta['book_name'], ' is ok !---------')

        image = 'images/{}.jpg'.format(file_name)

        chapter_list = response.css('dd a')
        number = 0
        for chapter in chapter_list:
            number += 1
            chapter_name = chapter.css('a::text').extract()[0]
            chapter_url = chapter.css('a::attr(href)').extract()[0]
            chapter_url = response.url + chapter_url
            meta.update({
                'author': author,
                'intro': intro,
                'image': image,
                'chapter_name': chapter_name,
                'number': number
            })
            yield scrapy.Request(chapter_url, meta=meta, callback=self.get_content)

    def get_content(self, response):
        meta = response.meta
        content = ''.join(re.findall('</a>最新章节！(.*)</div><center class="clear">', response.text, re.S))
        meta.update({
            'content': content
        })

        item = NovelSpiderItem()
        item['category_name'] = meta['category_name']  # 分类名
        item['book_name'] = meta['book_name']  # 书名
        item['author'] = meta['author']  # 作者
        item['intro'] = meta['intro']  # 简述
        item['chapter_name'] = meta['chapter_name']  # 章节名
        item['number'] = meta['number']  # 章节排序
        item['content'] = meta['content']  # 内容
        item['image'] = meta['image']  # 图片地址
        return item
