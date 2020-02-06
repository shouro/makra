# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from minispider.models import Article, db_connect, create_table
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem
import json
import codecs
from datetime import timezone
import dateutil.parser


class MinispiderPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.makeSession = sessionmaker(bind=engine)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item.get('status') == 200 and item.get('article'):
            try:
                item['date_published'] = dateutil.parser.parse(item.get('date_published')).astimezone(timezone.utc).replace(tzinfo=None)
                item['date_modified'] = dateutil.parser.parse(item.get('date_modified')).astimezone(timezone.utc).replace(tzinfo=None)
            except Exception:
                item['date_published'] = None
                item['date_modified'] = None
                spider.logger.warning('Date parsing failed, URL: {0}'.format(item.get('url')))

            session = self.makeSession()
            found = session.query(Article).filter(Article.uid == item.get('uid')).first()
            if not found:
                article = Article(**item)
                try:
                    session.add(article)
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()
            else:
                session.close()
                spider.logger.warning('Droping duplicate item: {}'.format(item.get('url')))
        else:
            spider.logger.warning('Failed URL: {0}'.format(item.get('url')))
            raise DropItem('Need to investigate')
        return item

    def close_spider(self, spider):
        pass
