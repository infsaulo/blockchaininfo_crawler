from scrapy.item import Item, Field

class BlockchaininfoCrawlerItem(Item):

    address = Field()
    tag = Field()
    url = Field()
    verified = Field()