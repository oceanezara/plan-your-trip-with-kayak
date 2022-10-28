import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import os

class Gps(scrapy.Spider):

    # Name of your spider
    name = "gps"

    # Url to start your spider from 
    start_urls = [
        'https://nominatim.openstreetmap.org/ui/search',
    ]

 # Callback function that will be called when starting your spider
    # It will get text, author and tags of all the <div> with class="quote"
    def parse(self, response):
        cities = [  "Mont Saint Michel",
                    "St Malo",
                    "Bayeux",
                    "Le Havre",
                    "Rouen",
                    "Paris",
                    "Amiens",
                    "Lille",
                    "Strasbourg",
                    "Chateau du Haut Koenigsbourg",
                    "Colmar",
                    "Eguisheim",
                    "Besancon",
                    "Dijon",
                    "Annecy",
                    "Grenoble",
                    "Lyon",
                    "Gorges du Verdon",
                    "Bormes les Mimosas",
                    "Cassis",
                    "Marseille",
                    "Aix en Provence",
                    "Avignon",
                    "Uzes",
                    "Nimes",
                    "Aigues Mortes",
                    "Saintes Maries de la mer",
                    "Collioure",
                    "Carcassonne",
                    "Ariege",
                    "Toulouse",
                    "Montauban",
                    "Biarritz",
                    "Bayonne",
                    "La Rochelle"]
        i = 0
     
        for city in cities:

            yield {
                'id': i,
                'city': city,
                'gps': response.xpath(f'/html/body/header/nav/div/div[1]/a/h1/text()').get(),
            }

            i = i +1

        
        # try:
        #     # Select the NEXT button and store it in next_page
        #     # Here we include the class of the li tag in the XPath
        #     # to avoid the difficujlty with the "previous" button
        #     next_page = response.xpath('/html/body/div/div[2]/div[1]/nav/ul/li[@class="next"]/a').attrib["href"]
        # except KeyError:
        #     # In the last page, there won't be any "href" and a KeyError will be raised
        #     logging.info('No next page. Terminating crawling process.')
        # else:
        #     # If a next page is found, execute the parse method once again
        #     yield response.follow(next_page, callback=self.parse)

#//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[1]/td[2]
#//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[2]/td[2]


# Name of the file where the results will be saved
filename = "gps.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('kayak/'):
        os.remove('kayak/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'kayak/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(Gps)
process.start()