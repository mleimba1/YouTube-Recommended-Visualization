# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#from scrapy.exporters import CsvItemExporter

####from scrapy.exporters import CsvItemExporter
####FILE = "items.csv"
####class CsvPipeline(object):
####    def __init__(self):
####        self.file = open(FILE, 'a')
####        self.exporter = CsvItemExporter(self.file)
####        self.exporter.start_exporting()
####
####    def close_spider(self, spider):
####        self.exporter.finish_exporting()
####        self.file.close()
####
####    def process_item(self, item, spider):
####        self.exporter.export_item(item)
####        return item
##
##import csv
##
##FILE = "items.csv"
##class CsvPipeline(object):
##    def __init__(self):
##        self.file = open(FILE, 'a')
##        self.exporter = csv.DictWriter(self.file, ['id','title','count','duration','uploaddate','category','upnext','recommends'])
##
##    def close_spider(self, spider):
##        self.file.close()
##
##    def process_item(self, item, spider):
##        self.exporter.writerow(item)
##        return item
##
### From https://gist.github.com/abevoelker/1060649
##from scrapy import signals
##from scrapy.utils.serialize import ScrapyJSONEncoder
##from scrapy.xlib.pydispatch import dispatcher
##
##from pika import ConnectionParameters
##from pika import BlockingConnection
##
##from twisted.internet.threads import deferToThread
##
##import json as simplejson
###import settings
##
####class MessageQueuePipeline(object):
####    """Emit processed items to a RabbitMQ exchange/queue"""
####    def __init__(self, host_name, port, userid, password, virtual_host, encoder_class):
####        self.q_connection = BrokerConnection(
####            ConnectionParameters(host=host_name, port=port,
####                        userid=userid, password=password,
####                        virtual_host=virtual_host))
####        self.encoder = encoder_class()
####        dispatcher.connect(self.spider_opened, signals.spider_opened)
####        dispatcher.connect(self.spider_closed, signals.spider_closed)
####
####    @classmethod
####    def from_settings(cls, settings):
####        host_name = settings.get('BROKER_HOST')
####        port = settings.get('BROKER_PORT')
####        userid = settings.get('BROKER_USERID')
####        password = settings.get('BROKER_PASSWORD')
####        virtual_host = settings.get('BROKER_VIRTUAL_HOST')
####        encoder_class = settings.get('MESSAGE_Q_SERIALIZER', ScrapyJSONEncoder)
####        return cls(host_name, port, userid, password, virtual_host, encoder_class)
####
####    def spider_opened(self, spider):
####        self.publisher = self.q_connection.channel()
######        self.publisher = Publisher(connection=self.q_connection,
######                        exchange="",
######                        routing_key=spider.name)
####
####    def spider_closed(self, spider):
####        self.publisher.close()
####
####    def process_item(self, item, spider):
####        return deferToThread(self._process_item, item, spider)
####
####    def _process_item(self, item, spider):
####        self.publisher.send(self.encoder.encode(dict(item)))
####        return item
##
##from io import StringIO
##class MessageQueuePipeline(object):
##    """Emit processed items to a RabbitMQ exchange/queue"""
##    def __init__(self, host_name, port, userid, password, virtual_host, encoder_class):
##        self.connection = BlockingConnection()
##        self._file = StringIO()
##        self.encoder = self.exporter = csv.DictWriter(self.file, ['id','title','count','duration','uploaddate','category','upnext','recommends'])
##        dispatcher.connect(self.spider_opened, signals.spider_opened)
##        dispatcher.connect(self.spider_closed, signals.spider_closed)
##
##    @classmethod
##    def from_settings(cls, settings):
##        host_name = settings.get('BROKER_HOST')
##        port = settings.get('BROKER_PORT')
##        userid = settings.get('BROKER_USERID')
##        password = settings.get('BROKER_PASSWORD')
##        virtual_host = settings.get('BROKER_VIRTUAL_HOST')
##        encoder_class = settings.get('MESSAGE_Q_SERIALIZER', ScrapyJSONEncoder)
##        return cls(host_name, port, userid, password, virtual_host, encoder_class)
##
##    def spider_opened(self, spider):
##        self.channel = self.connection.channel()
##
##    def spider_closed(self, spider):
##        self.publisher.close()
##
##    def process_item(self, item, spider):
##        self.encoder.writerow(dict(item))
##        self.publisher.send(self._file.getvalue())
##        self._file.truncate(0)
##        self._file.seek(0)
##        
##        return item


#https://medium.com/python4you/rabbitmq-scrapy-item-publisher-in-python-4c66a985e3cb
import json
#https://github.com/artemrys/scrapy-rabbitmq-publisher
import pika
from scrapy.utils.serialize import ScrapyJSONEncoder

class RabbitMQItemPublisherPipeline(object):
    def __init__(self, host, port, user, password, virtual_host, exchange, routing_key, queue):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.virtual_host = virtual_host
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host,
                                               self.port,
                                               self.virtual_host,
                                               credentials)
        # Connecting to RabbitMQ
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue = queue
        # Declaring RabbitMQ exchange
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type="direct",
                                      durable=True)
        # Decaling RabbitMQ queue
        self.channel.queue_declare(queue=queue,
                                   durable=True)
        # Binding exchange + routing_key = queue
        self.channel.queue_bind(exchange=exchange,
                                routing_key=routing_key,
                                queue=queue)
        self.encoder = ScrapyJSONEncoder()

    @classmethod
    def from_crawler(cls, crawler):
        # Creating a RabbitMQItemPublisherPipeline
        return cls(
            host=crawler.settings.get("RABBITMQ_HOST"),
            port=crawler.settings.get("RABBITMQ_PORT"),
            user=crawler.settings.get("RABBITMQ_USER"),
            password=crawler.settings.get("RABBITMQ_PASSWORD"),
            virtual_host=crawler.settings.get("RABBITMQ_VIRTUAL_HOST"),
            exchange=crawler.settings.get("RABBITMQ_EXCHANGE"),
            routing_key=crawler.settings.get("RABBITMQ_ROUTING_KEY"),
            queue=crawler.settings.get("RABBITMQ_QUEUE"),
        )

    def close_spider(self, spider):
        # Closing RabbitMQ channel and connection
        self.channel.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Encoding item dict using Scrapy JSON Encoder
        data = self.encoder.encode(item)
        # Publishing item to exchange + routing_key = queue
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=data,
        )
        # Returning item to be processed
        return item
