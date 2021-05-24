import scrapy
from scrapy_redis.spiders import RedisSpider
import re


class DangdangSpider(RedisSpider):
    name = 'travel'
    allowed_domains = ['dgguolv.com']
    # start_urls = ['http://www.dgguolv.com/Tourism/tour_1.html']
    redis_key = 'travel'

    def parse(self, response):
        # a_list = response.xpath('//td[@align="center"]/a')
        # for a in a_list:
        #     item = {}
        #     url = a.xpath('./@href').extract_first()
        #     name = a.xpath('./text()').extract_first()
        #     if "List" in url:
        #         item["url"] = "http://www.dgguolv.com/" + url
        #         item["name"] = name
        #         yield scrapy.Request(item["url"], callback=self.parse_line, meta={"item": item})
        item = {}
        item["name"] = "海岛游轮"
        url = "http://www.dgguolv.com/Tourism/Tour_5.html"
        yield scrapy.Request(url, callback=self.parse_line, meta={"item": item})

    def parse_line(self, response):
        item = response.meta["item"]

        a_list = response.xpath('//a[@class="product_detail"]')
        if len(a_list) > 0:
            for a in a_list:
                img = a.xpath('../preceding-sibling::td/a/img/@src').extract_first()
                if img:
                    item["img"] = "http://www.dgguolv.com" + img
                else:
                    item["img"] = "无"
                item["lname"] = a.xpath('./text()').extract_first()
                item["lurl"] = "http://www.dgguolv.com" + a.xpath('./@href').extract_first()
                item["sec"] = a.xpath('../text()').extract_first()
                yield scrapy.Request(item["lurl"], callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        td = response.xpath('//td[@class="Bmodebg"]')
        price = td.xpath('./div/text()').extract()[1]
        price = re.findall('\d+', price)
        to_time = td.xpath('./div/span/text()').extract_first()
        if price:
            price = price[0]
        else:
            price = "0"
        item["price"] = int(price)
        item["to_time"] = int(to_time)
        detail = re.findall('<span class="t14">特色行程</span>(.*)<hr style="BORDER: #999999 1px dotted;" size="0">', td.extract_first(), re.S)[0]
        item["detail"] = detail
        # print(item)
        yield item
