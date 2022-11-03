import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import os
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

   

class booking(scrapy.Spider):
    # Name of your spider
    name = "booking"

    start_urls = [
        'https://www.booking.com/'
    ]


    def parse(self, response):
        file = open('/Users/oceane/Desktop/plan-your-trip-with-kayak/kayak/kayak/top_city_names.txt', 'r')
        cities = file.readlines()
        for city in cities:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': city},
                callback=self.after_search
            )

    def after_search(self, response):
        for path in response.xpath('//*[@data-testid="property-card"]'):
        
            url = path.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a').attrib['href']

             # call parse_details and pass all of the above to it
            dict_hotel = {
                'url' : url
            } 

            try:
                yield response.follow(url = url, callback = self.parse_detail, cb_kwargs = {'dic':dict_hotel})
            
            except:
                yield dict_hotel
          


    def parse_detail(self,response,dic):

        lat_lon = response.css('a.jq_tooltip.loc_block_link_underline_fix.bui-link.show_on_map_hp_link.show_map_hp_link').attrib['data-atlas-latlng']
        dic['coordinates'] = lat_lon
        yield dic



filename = "hotel_url.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir():
    os.remove(filename)


# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/lahotel_url/topics/settings.html?highlight=settings#settings
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