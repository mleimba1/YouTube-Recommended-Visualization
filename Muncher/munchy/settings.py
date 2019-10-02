# -*- coding: utf-8 -*-

# Scrapy settings for munchy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'munchy'

SPIDER_MODULES = ['munchy.spiders']
NEWSPIDER_MODULE = 'munchy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'munchy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 1000

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'munchy.pipelines.CsvPipeline': 300,
    #'munchy.pipelines.RabbitMQItemPublisherPipeline': 400,
}

HTTPCACHE_ENABLED = False

REACTOR_THREADPOOL_MAXSIZE = 20
DEPTH_LIMIT = 5
LOG_LEVEL = 'INFO'

# Messaging config

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_VIRTUAL_HOST = "/"
RABBITMQ_EXCHANGE = "scrapy"
RABBITMQ_ROUTING_KEY = "item"
RABBITMQ_QUEUE = "item"
