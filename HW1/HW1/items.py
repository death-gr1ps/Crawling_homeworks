# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PointItem(scrapy.Item):
    """Dataclass containes information about merchant point"""
    mcc           = scrapy.Field()
    merchant_name = scrapy.Field()
    address       = scrapy.Field()

class OrganizationItem(scrapy.Item):
    """Dataclass containes information about organization"""
    org_name        = scrapy.Field()
    org_description = scrapy.Field()
    source_url      = scrapy.Field()
    points          = scrapy.Field()
