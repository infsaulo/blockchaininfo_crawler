from scrapy.item import Item, Field

class TagCrawlerItem(Item):

    address = Field()
    tag = Field()
    url = Field()
    verified = Field()