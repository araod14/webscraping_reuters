import scrapy
from urllib.parse import urljoin


class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['reuters.com']
    start_urls = ['http://reuters.com/']
    custom_settings = {
        'FEED_URI' : 'reuters.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'DanielJoseMartinez',
    }

    def parse(self, response):
        topics = response.xpath('//div[@class="topic__header__3T_p2"]/h2/a/text()').getall()  
        usnews = response.xpath('//li[@class="story-collection__story__LeZ29 story-collection__default__G33_I story-collection__with-spacing__1E6N5"]/div[@class="media-story-card__hub__3mHOR story-card"]/div[@class="media-story-card__body__3tRWy"]/h3/a/text()').getall()
        usnewslink = response.xpath('//li[@class="story-collection__story__LeZ29 story-collection__default__G33_I story-collection__with-spacing__1E6N5"]/div[@class="media-story-card__hub__3mHOR story-card"]/div[@class="media-story-card__body__3tRWy"]/h3/a/@href').getall()
        
        yield {
            "Title" : topics,
            "news": usnews,
            "Links": usnewslink
        }
        for link in reversed(usnewslink):
            absolute_link = urljoin(response.url, link)
            yield scrapy.Request(url=absolute_link, callback=self.parse_page)



    def parse_page(self, response):  
        newsbody = response.xpath('//div[@class="article-body__content__17Yit"]/p/text()').getall()

        yield {
            "body":newsbody
        }