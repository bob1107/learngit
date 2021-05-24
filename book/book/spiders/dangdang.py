import scrapy
from scrapy_redis.spiders import RedisSpider
import re


class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://dangdang.com/']
    redis_key = 'dangdang'

    def parse(self, response):
        div_list = response.xpath('//div[@class="con flq_body"]/div')
        for div in div_list:
            a_list = div.xpath('.//dl[@class="inner_dl"]/dd/a')
            for a in a_list:
                item = {}
                item["分类"] = a.xpath('./@title').extract_first()
                item["分类链接"] = a.xpath('./@href').extract_first()

                yield scrapy.Request(item["分类链接"], callback=self.parse_book, meta={"item": item})

    def parse_book(self, response):
        item = response.meta["item"]
        li_list = response.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            item["book_url"] = li.xpath('./a/@href').extract_first()
            if item["book_url"] is not None:
                yield scrapy.Request(item["book_url"], callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        item["name"] = response.xpath('//h1/@title').extract_first()
        item["desc"] = response.xpath('//h2/@title').extract_first()
        if item["desc"] is None:
            item["desc"] = ""
        item["author"] = ",".join(response.xpath('//span[@id="author"]/a/text()').extract())
        item["pub"] = response.xpath('//span[@dd_name="出版社"]/a/text()').extract_first()
        item["date_time"] = response.xpath('//div[@class="messbox_info"]/span[3]/text()').extract_first()
        if item["date_time"]:
            item["date_time"] = re.sub("\\xa0", "",
                                       response.xpath('//div[@class="messbox_info"]/span[3]/text()').extract_first())
        item["comm_num"] = response.xpath('//a[@id="comm_num_down"]/text()').extract_first()
        item["price"] = response.xpath('//p[@id="dd-price"]/text()').extract()
        if item["price"] is not None and len(item["price"]) > 1:
            item["price"] = item["price"][-1]
        else:
            item["price"] = ""
        item["author"] = [i.strip() for i in item["author"] if len(item["author"]) > 0]
        print(item)
        yield item
