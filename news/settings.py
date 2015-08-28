# Scrapy settings for news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'news.pipelines.JsonWithEncodingTencentPipeline': 300,
    'news.pipelines.MySQLStoreCnblogsPipeline': 30,
}
DOWNLOAD_DELAY = 1

COOKIES_ENABLED=False
LOG_LEVEL = 'INFO'
# start MySQL database configure setting
MYSQL_HOST = '192.168.210.167'
MYSQL_DBNAME = 'db_hsb_grab'
MYSQL_USER = 'yunneng'
MYSQL_PASSWD = 'yunneng999'
# end of MySQL database configure setting  rdsi0814385qufqu31to.mysql.rds.aliyuncs.com
