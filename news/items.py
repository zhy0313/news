# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TencentItem(Item):
    name = Field()
    url = Field()
    img = Field()
    companyName = Field()
    foundingTime = Field()
    legalRepresentative = Field()
    manager = Field()
    registeredCapital = Field()
    netAssets = Field()
    netCapital = Field()
    registeredAddress = Field()
    salesDepartments = Field()
    officeAddress = Field()
    postCode = Field()
    website = Field()
    email = Field()
    license = Field()
    CSRSbusiness = Field()
    neeqBusiness = Field()
    survey = Field()

class  EastMoneyItem(Item):
    title = Field()
    info = Field()
    content = Field()
    source = Field()
    source_type = Field()
    keyword = Field()
    description = Field()
    status = Field()
    create_time = Field()
    link = Field()