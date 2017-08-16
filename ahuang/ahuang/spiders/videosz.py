import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 

class SiteVideoszSpider(scrapy.Spider):

	name = "videosz"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 0.5,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        }
	
	base_url = "http://www.videosz.com/us/scenes/best-rated/{}"
	
	def start_requests(self):
		for idx in xrange(1,2787):
			yield scrapy.Request(self.base_url.format(idx),self.parse_cover)
	
	def parse_cover(self,response):
		hrefs = response.css(".border_pad_frame a::attr(href)").extract()
		for href in hrefs:
			yield scrapy.Request(urljoin("http://www.videosz.com",href),self.parse_images)

	def parse_images(self,response):
		imgs = response.css(".preview_thumb img::attr(src)").extract()
		for img in imgs:
			imgurl = img.replace('thumbs4/','')
			yield ImageItem(url=imgurl,created=datetime.now(),source=response.url)