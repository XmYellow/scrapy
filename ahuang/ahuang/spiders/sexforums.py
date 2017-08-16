import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url


class SiteSexforumsSpider(scrapy.Spider):

	name = "sexforums"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        }
	
	base_url = "https://www.sexforums.com/gallery/?sort=rated&time=year&page={}"
	
	def start_requests(self):
		for idx in xrange(1,420):
			yield scrapy.Request(self.base_url.format(idx),self.parse_cover)

	
	def parse_cover(self,response):
		hrefs = response.css(".userphoto a::attr(href)").extract()
		for href in hrefs:
			yield scrapy.Request(href,self.parse_images)

	def parse_images(self,response):
		imgs = response.css("#large-image img::attr(src)").extract()
		for img in imgs:
			yield ImageItem(url=img,created=datetime.now(),source=response.url)

