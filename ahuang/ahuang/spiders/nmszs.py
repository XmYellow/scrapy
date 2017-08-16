import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url


class SiteNmszsSpider(scrapy.Spider):

	name = "nmszs"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }

	start_urls=["http://xiamen.nmszs.cn/design/list-htm-fid-2-page-1-k1-0-k2-0-k3-0.html"]
	
	pattern = re.compile(r'-page-\d+')

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url,self.parse_cover)

	def parse_page(self,response):
		imgs = response.css(".xdbc_main_content img::attr(src)").extract()
		for img in imgs:
			yield ImageItem(url=img,created=datetime.now(),source=response.url)

	def parse_cover(self,response):
		for r in self.parse_bigimg(response):
			yield r
		pages = response.css(".pages a::text").extract()[-2]
		total = int(pages.split("/")[1])
		for idx in xrange(2,total+1):
			yield scrapy.Request(re.sub(self.pattern,"-page-{}".format(idx),response.url),self.parse_bigimg)

	def parse_bigimg(self,response):
		bigurls = response.css(".trip-list-v2 a::attr(href)").extract()
		for bigurl in bigurls:	
			yield scrapy.Request(urljoin(response.url,bigurl),callback=self.parse_page,headers=self.headers)