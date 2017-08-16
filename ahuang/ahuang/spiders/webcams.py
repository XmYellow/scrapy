import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url

class SiteWebcamsSpider(scrapy.Spider):

	name = "webcams"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }
	
	base_url = "http://www.webcams.com/latestimages/{}"
	
	def start_requests(self):
		for idx in xrange(1,161):
			yield scrapy.Request(self.base_url.format(idx),self.parse_images)
	
	def parse_images(self,response):
		imgs = response.css(".img-responsive::attr(src)").extract()
		for img in imgs:
			yield ImageItem(url=img,created=datetime.now(),source=response.url)

