import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url

class Site3D66Spider(scrapy.Spider):

	name = "3d66"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 0.5,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }

	start_urls=["http://www.3d66.com/model_1_160.html"]

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url,self.parse_cover)

	def parse_page(self,response):
		imgs = response.css(".preview-list img::attr(data-bimgsrc)").extract()
		for img in imgs:
			yield ImageItem(url=img,created=datetime.now(),source=response.url)

	def parse_cover(self,response):
		for r in self.parse_bigimg(response):
			yield r

		pages = response.css("#softpagenav a::attr(href)").extract()
		if len(pages) : 
			pages = pages[:-1]

		for url in pages:
			yield scrapy.Request(urljoin(response.url,url),self.parse_bigimg)

	def parse_bigimg(self,response):
		bigurls = response.css(".prolistM a.bimg::attr(href)").extract()
		for bigurl in bigurls:	
			yield scrapy.Request(urljoin(response.url,bigurl),callback=self.parse_page,headers=self.headers)