# Scrapy settings for book project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'book'

SPIDER_MODULES = ['book.spiders']
NEWSPIDER_MODULE = 'book.spiders'

DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
REDIS_URL = 'redis://192.168.0.222:6379'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = "WARNING"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    # 'referer': 'https://tieba.baidu.com/',
    'referer': 'https://quanxiaoshuo.com/',
    # 'Cookie': 'PSTM=1620137500; BAIDUID=C7356A77FE9F6333761FFF933DE92D80:FG=1; BIDUPSID=E7424236559FE63D2115D4C964E4D617; __yjs_duid=1_95327265e1a791c7e9edefb91db387031620137876066; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID_BFESS=m68OJeC626k1rcJeCSISMZfw0eo83InTH6ORIkrz31O6edpx9a26EG0PSU8g0KubIp7SogKK3gOTHxDF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJAHVCt-tD_3fP36qR7B-nF3KgT22-us2Hcm2hcH0KLKfDIx-pt5bftm5hruXt5ftITiBInlJMb1MRLRDtD55q_X5HAthfQnbGTNop5TtUtW8DnTDMRh-4_wMx6yKMnitKv9-pny3pQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuD68hD6cBeH-s5JvK-T4X3buQtK0M8pcNLTDKetIOXa59KxJgLIvuhJQ5tncNjU0GhlO1jx4wjajNat6WyHOC0pjHHl3GVq5jDh3ob6ksD-RC5frj2Kjy0hvctb3cShn9QMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2b6QhDGAHJT8OtnCsW6uhHJREetTv5DTjhPrMhHDOWMT-0bFH_Jkh-JOkeqObyqbYW4KWDMoyqTJAaHn7_q74WRvKJC8lXTjqbb8befLHtfQxtNRg-CnjtpvhHlTxjpbobUPUDUJ9LUvO3gcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLK-oj-D8xDjQP; bdshare_firstime=1621239662542; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1621239663; BAIDUID_BFESS=B350B25C76FE6B0AF3DC3835DE86CC82:FG=1; BAIDU_WISE_UID=wapp_1621247592037_939; H_PS_PSSID=33839_33969_31253_34004_33607_34026; delPer=0; PSINO=7; BA_HECTOR=ak2ha02k05a08galev1ga4oqc0q; wise_device=0; USER_JUMP=-1; st_key_id=17; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1621252488,1621252816,1621255353,1621255384; tb_as_data=56e2054fbcddcae70736c8f9f2456f07d5024756fd42de6bee2f21a9f20119449b2db6641e134d04688b24dc685bc214a6af21e18973208acf520edb4365d689b1a708763471fcd7b0d9708635262d0c59f362c337011d3b0fbc0d3d9e679a30dd18c460fad96e1095fd1d605db622ff; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1621255389; video_bubble0=1; ab_sr=1.0.0_Y2Q3NzAxYzkwMDUwZGJhMTJiOTBlMjgzNWZkMzFiN2Q1MjhhNWVmZGRiN2U3NmNmNWExZWRlMDViN2ZlYmMwYjhhNjEyMmRmZDE3YmI4NzBhZjAzMmRmNzljZWRlYjQy; st_data=7a8d9995dccb6f0683ceb43cc07789f893daec304c3d9968ae04f11bc20f9f0d8fd8d4c557d37116419a50eeaa36ec8c8ba08a172eeacd0e499a1cfb37324cc5fd2919586dd038aec2032dc50960109d158f0c7360921b41506cc61a698d88d6a3bf3a66506d3a449842a93fce1924600a38845cf29772edec202c03fb128f39; st_sign=73e86f3d'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'book.middlewares.BookSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'book.middlewares.BookDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'book.pipelines.BookPipeline': 300,
    # 'book.pipelines.TiebaPipeline': 300,
    # 'book.pipelines.XiaoshuoPipeline': 300,
    'book.pipelines.NovelSpiderPipeline': 300,
    # 'book.pipelines.TravelPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
