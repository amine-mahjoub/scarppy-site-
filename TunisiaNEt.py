import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
import logging

class TunisiaNetSpider(scrapy.Spider):
    name = "laptop"
    allowed_domains = ["tunisianet.com.tn"]
    start_urls = ["https://www.tunisianet.com.tn/702-ordinateur-portable"]

    def parse(self, response): 
        for selector in response.css('div.products.product-thumbs .item-product'):
            yield {
                'title': selector.css('h2.product-title a::text').get(),
                'price': selector.css('span.price::text').get(),
                'reference': selector.css('span.product-reference::text').get(),
                'image_url': selector.css('#js-product-list img.center-block.img-responsive::attr(src)').get()

            }


        next_page_link = response.css('a.next::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        else:
            logging.info('No more pages to scrape.')




def TunisiaNet_spider_result():
    TunisiaNet_results = []

    def crawler_results(item, **kwargs):
        TunisiaNet_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(TunisiaNetSpider)
    crawler_process.start()

    return TunisiaNet_results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    laptop_data = TunisiaNet_spider_result()

    if laptop_data:
        keys = laptop_data[0].keys()
        with open('laptop.csv', 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(laptop_data)
        logging.info('Data has been written to laptop.csv')
    else:
        print("No data to write.") 