import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import os
from scrapy.linkextractors import LinkExtractor


   

class booking(scrapy.Spider):
    # Name of your spider
    name = "booking"

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the first <div> with class="quote"

    def start_requests(self):
        # Defining cities
        cities =  ['Collioure', 'Cassis', 'Marseille', 'Bormes-les-Mimosas', 'Aigues-Mortes']
        # Creating urls from cities
        urls = []

        for city in cities:
            urls.append(f'https://www.booking.com/searchresults.fr.html?aid=304142&label=gen173nr-1FCAQoggJCGXNlYXJjaF9ib3JtZXMtbGVzLW1pbW9zYXNIDVgEaE2IAQGYAQ24AQfIAQzYAQHoAQH4AQOIAgGoAgO4ApGLhZsGwAIB0gIkMTU2MWY1NzctNmEyMi00ZjVjLWI3OGUtNDBjYTBiNmQ1OWRh2AIF4AIB&ss={city}&order=bayesian_review_score')

        
        # Launching crawling process for each city
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hotels = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div')
        for hotel in hotels:
            yield {
                'city': hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[2]/div[1]/a/span/span[1]/text()').get(),
                'name':hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
                'rating': hotel.xpath('div[1]/div[2]/div/div/div[2]/div[1]/a/span/div/div[1]/text()').get(),
                'url': hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/@href').extract_first(),
                'text_description': hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[4]/text()').get(),
                }
                
     
# hotel name,
# *   Url to its booking.com page,
# *   Its coordinates: latitude and longitude
# *   Score given by the website users
# *   Text description of the hotel
# Name of the file where the results will be saved
filename = "test.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir():
    os.remove(filename)


# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(booking)
process.start()