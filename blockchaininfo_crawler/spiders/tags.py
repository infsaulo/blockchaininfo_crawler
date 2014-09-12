from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from blockchaininfo_crawler.items import TagCrawlerItem

class TagSpider(CrawlSpider):
    name = 'tag'
    allowed_domains = ['blockchain.info']
    start_urls = ['http://blockchain.info/tags']

    rules = (
        Rule(SgmlLinkExtractor(allow=[r'/tags']),
             callback='parse_tags', follow=True),
    )


    def parse_tags(self, response):
        sel = Selector(response)

        tag_list = sel.xpath('//tr')
        for tag in tag_list:
            item = TagCrawlerItem()

            item['address'] = tag.xpath('td[1]/a/text()').extract()[0].strip()
            item['tag'] = tag.xpath('td[2]/span/text()').extract()[0].strip()
            item['url'] = tag.xpath('td[3]/a/@href').extract()[0].strip()
            is_verified = tag.xpath('td[4]/img/@src').extract()[0].strip()
            if 'red_cross' in is_verified:
                item['verified'] = False
            else:
                item['verified'] = True

            yield item

