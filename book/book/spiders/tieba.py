import scrapy
from scrapy_redis.spiders import RedisSpider
import re
from lxml import etree


class TbSpider(RedisSpider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    # start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=%E5%89%91%E7%81%B5%E6%B4%AA%E7%A6%8F%E5%8C%BA&pn=0&'] # 在响应中找到起始页的url
    redis_key = 'tieba'

    def parse(self, response):
        ul_str = re.findall(r'<ul id="thread_list"(.*)</ul>', response.text, re.S)[0]
        html = etree.HTML(ul_str)
        li_list = html.xpath('//li')
        for li in li_list:
            title = li.xpath(".//a[@class='j_th_tit ']/text()")
            if title != []:
                href = li.xpath(".//a[@class='j_th_tit ']/@href")
                if href:
                    href = "https://tieba.baidu.com" + href[0]
                yield scrapy.Request(
                    href,
                    callback=self.parse_detail,
                )

        next_url = re.findall('<a href="//(.*)" class="next', response.text)
        if next_url != []:
            next_url = "https://" + next_url[0]
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    def parse_detail(self, response):
        div_list = response.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
        if div_list != []:
            for div in div_list:
                item = {}
                context = div.xpath('.//div[@class="d_post_content j_d_post_content "]/text()').extract()
                if len(context) > 0:
                    name = div.xpath('.//li[@class="d_name"]/a/text()').extract_first()
                    context = ''.join(context[0]).strip()
                    if context:
                        if '私聊' in context or '推广' in context or '陪玩' in context or 'app' in context or 'V' in context or 'v' in context or '语音' in context or '星球' in context or '联系方式' in context or '交友' in context or '引流' in context or '聊天' in context or '社交' in context or '资源' in context or '直播' in context or '主播' in context or '平台' in context:
                            item['name'] = name
                            item['content'] = context
                            item['url'] = response.url
                            yield item

        next_url = re.findall('<a href="(.*)">下一页</a>', response.text)
        if next_url != []:
            next_url = "https://tieba.baidu.com" + next_url[0]
            yield scrapy.Request(
                next_url,
                callback=self.parse_detail,
            )
