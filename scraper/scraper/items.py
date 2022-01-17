import scrapy


class Job(scrapy.Item):

    summary_data = scrapy.Field()
    company = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()

