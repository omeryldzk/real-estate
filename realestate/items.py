import scrapy

class RealestateItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    location = scrapy.Field()
    property_type = scrapy.Field()
    rooms = scrapy.Field()
    size = scrapy.Field()
    age = scrapy.Field()
    floor = scrapy.Field()
    date = scrapy.Field()
    image_url = scrapy.Field()
    agency_logo = scrapy.Field()
