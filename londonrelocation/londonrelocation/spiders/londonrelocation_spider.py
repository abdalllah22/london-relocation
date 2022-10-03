import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..items import LondonrelocationItem


class londonrelocationSpider(scrapy.Spider):
  name = 'londonrelocation'
  allowed_domains = ['londonrelocation.com']
  start_urls = ['https://londonrelocation.com/properties-to-rent/']
  
  def parse(self, response):
    for start_url in self.start_urls:
      yield Request(
        url = start_url,
        callback = self.parse_areas
      )
  
  def parse_areas(self, response):
    area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
    # print(area_urls)
    for area_url in area_urls:
      yield Request(
        url = area_url,
        callback = self.parse_pages_for_area
      )
  
  def parse_pages_for_area(self, response):
        # Write your code here and remove `pass` in the following line
    for i in [1, 2]:
      page_number = response.url+'&pageset='+str(i)
      yield scrapy.Request(
        url = page_number,
        callback = self.parse_page
      )
  
  def parse_page(self, response):
    urls = ['https://londonrelocation.com' + url_property for url_property in response.css(".h4-space a::attr(href)").getall()]
    for url in urls:
      yield scrapy.Request(
        url = url,
        callback = self.parse_property
      )
  
  def parse_property(self, response):
    items = LondonrelocationItem()
    
    title = response.css("h1::text").get()
    price = float(response.css("h3::text").get().split()[0][1:])
    url = response.url
    
    items['title'] = title
    items['price'] = price
    items['url'] = url
    
    yield items

