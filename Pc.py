import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

class PcSpider(scrapy.Spider):
    name = "Pc"
    allowed_domains = ["mytek.tn"]
    start_urls = ["https://www.mytek.tn/informatique/ordinateurs-portables.html"]

    def parse(self, response):
        for selector in response.css('li.product-item'):
            yield {
                'title': selector.css('a.product-item-link::text').get(),
                'price': selector.css('span.price::text').get(),
                'reference': selector.css('div.skuDesktop::text').get(),
                'description': selector.css('div.product-item-description::text').get()
            }

        next_page_link = response.css('li.pages-item-next >a::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        else:
            self.log('No more pages to scrape.')

def Pc_spider_result():
    Pc_results = []

    def crawler_results(item, **kwargs):
        Pc_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(PcSpider)
    crawler_process.start()
    return Pc_results

if __name__ == '__main__':
    Pc_data = Pc_spider_result()

    if Pc_data:
        keys = Pc_data[0].keys()
        with open('My_Tek.csv', 'w', newline='', encoding='utf-8') as output_file_name:
            writer = csv.DictWriter(output_file_name, fieldnames=keys)
            writer.writeheader()
            writer.writerows(Pc_data)
    else:
        print("No data to write.")