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
        return scrapy.FormRequest.from_response(
            response,
            formdata={'ss': 'Marseille'},
            callback=self.after_search
        )

    def after_search(self, response):
        for path in response.xpath('//*[@data-testid="property-card"]'):
        
            url = path.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a').attrib['href']

             # call parse_details and pass all of the above to it
            dic = {
                'url' : url
            } 

            try:
                yield response.follow(url = url, callback = self.parse_detail, cb_kwargs = {'dic':dic})
            
            except:
                yield dic
          


    def parse_detail(self,response,dic):

        lat_lon = response.css('a.jq_tooltip.loc_block_link_underline_fix.bui-link.show_on_map_hp_link.show_map_hp_link').attrib['data-atlas-latlng']
        dic['gps'] = lat_lon
        yield dic

       

  

            # yield response.follow(url=url, callback=self.parse_hotel, cb_kwargs={'dic' : hotel_dict})
          
    # def parse_hotel(self, response):
    #     yield {
    #         **response.meta,
    #         'hotel_name': 'hello'
    #     }
    #     print(response)
          
    
        # url=response.request.meta.hotel_dict.url
        # rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        # for el in url:
        #     name=row.xpath(".//td[1]/text()").get()
  
        #     yield{
        #         'country_name': name,
                
        #     }
    

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