import scrapy
from scrapy_redis.spiders import RedisSpider
import re
from copy import deepcopy


class XiaoshuoSpider(RedisSpider):
    name = 'xiaoshuo'
    allowed_domains = ['quanxiaoshuo.com']
    # start_urls = ['https://quanxiaoshuo.com/']
    redis_key = 'xiaoshuo'

    def parse(self, response):
        li_list = response.xpath('//div[@class="meun"]/ul/li')
        for li in li_list:
            item = {}
            title = li.xpath('./a/text()').extract_first()
            url = 'https:' + li.xpath('./a/@href').extract_first()
            if title != '首页' and title != '点击榜' and title != '最新入库' and title != '最新更新':
                item['fenlei'] = title
                yield scrapy.Request(url, callback=self.parse_book, meta={'item': item})

    def parse_book(self, response):
        item = response.meta['item']
        ul_list = response.xpath('//ul[@class="list_content "]')
        for ul in ul_list:
            item['book_name'] = ul.xpath('./li[@class="cc2"]/a/text()').extract_first()
            book_url = 'https://quanxiaoshuo.com' + ul.xpath('./li[@class="cc2"]/a/@href').extract_first()
            item['author'] = ul.xpath('./li[@class="cc4"]/a/text()').extract_first()
            yield scrapy.Request(book_url, callback=self.parse_chapter, meta={'item': item})

        next_url = response.xpath('//a[@class="current"]')
        if next_url is not None:
            next_url = next_url.xpath('./following-sibling::a[1]/@href').extract_first()
            next_url = "https://quanxiaoshuo.com" + next_url
            yield scrapy.Request(next_url, callback=self.parse_book, meta={'item': deepcopy(item)})

    def parse_chapter(self, response):
        item = response.meta['item']
        div_list = response.xpath('//div[@class="chapter"]')
        desc = response.xpath('//div[@class="desc"]/text()').extract()
        desc = "".join(desc).strip()
        item["desc"] = desc
        number = 0
        for div in div_list:
            number += 1
            item['chapter_name'] = div.xpath('./a/text()').extract_first()
            chapter_url = 'https://quanxiaoshuo.com' + div.xpath('./a/@href').extract_first()
            item["number"] = number
            yield scrapy.Request(chapter_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        content = \
        re.findall(r'</script></td></tr></table>\r\n</div>\r\n\r\n (.*)<div style="color:#ff6600;font-size:16px"><br/>',
                   response.text, re.S)[0].strip()
        item["content"] = content
        yield item
