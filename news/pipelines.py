# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors


class JsonWithEncodingTencentPipeline(object):

    def __init__(self):
        self.east_file = codecs.open('east.json', 'w', encoding='utf-8')

    def process_item(self, item, spider): 
        self.east_file.write(json.dumps(dict(item), ensure_ascii=False) + "\n")
        return item

    def spider_closed(self, spider):
        self.file.close()
        self.east_file.close()

class MySQLStoreCnblogsPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # 
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d
    # 
    def _do_upinsert(self, conn, item, spider):
        link = self._get_link(item)
        #print link
        #now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from hsb_grab_news where linkmd5 = %s
        """, (link, ))
        ret = conn.fetchone()
        if ret:
            #pass
            conn.execute("""
                update hsb_grab_news set title = %s, info = %s, content = %s, source = %s, source_type = %s, keyword = %s, description = %s where linkmd5 = %s
            """, (item['title'], item['info'], item['content'], item['source'], item['source_type'], item['keyword'], item['description'], link))
            #print """
            #    update hsb_grab_news set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where link = %s
            #""" 
            #,(item['title'], item['description'], item['link'], item['link'], now, link)
        else:
            conn.execute("""
                insert into hsb_grab_news (title, info, content , source, source_type, keyword, description, link, linkmd5) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (item['title'], item['info'], item['content'], item['source'], item['source_type'], item['keyword'], item['description'], item['link'], link))
            #print """
            #    insert into hsb_grab_news (title, info, content , source, source_type, keyword, description, link, linkmd5) 
            #    values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            #"""
            #, (item['title'], item['info'], item['content'], item['source'], item['source_type'], item['keyword'], item['description'], item['link'], link)
    # 
    def _get_link(self, item):
        # 
        return md5(item['link']).hexdigest()
    # 
    def _handle_error(self, failue, item, spider):
        log.err(failure)