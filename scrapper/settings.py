# -*- coding: utf-8 -*-

# Scrapy settings for scrapper project

BOT_NAME = 'scrapper'
SPIDER_MODULES = ['scrapper.spiders']
NEWSPIDER_MODULE = 'scrapper.spiders'

# Splash settings
SPLASH_URL = 'http://splash:8050'  # <-- Splash instance URL from Scrapy Cloud
APIKEY = ''  # <-- your API key
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

LOG_ENABLED = True
LOG_STDOUT = True
