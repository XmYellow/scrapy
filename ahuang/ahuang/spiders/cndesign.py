import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url

class SiteCndesignSpider(scrapy.Spider):

	name = "cndesign"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }

	start_urls=["http://sn.cndesign.com"]

	pattern = re.compile(r'\d+')
	detailpatt = re.compile(r'_\d+')

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url,self.parse_cover)

	def parse_page(self,response):
		imgs = response.css(".detail_box img::attr(src)").extract()
		for img in imgs:
			yield ImageItem(url=urljoin(response.url,img),created=datetime.now(),source=response.url)

	def parse_depage(self,response):
		hrefs = response.css(".paging_ul a.paging_a::attr(href)").extract()
		len(hrefs)
		if len(hrefs)>=4:
			for idx in xrange(2,len(hrefs)-2):
				yield scrapy.Request(urljoin(response.url,re.sub(self.detailpatt,"_{}".format(idx),hrefs[-3])),self.parse_page)
		if len(hrefs)<4:
			for idx in xrange(2,len(hrefs)-1):
				yield scrapy.Request(urljoin(response.url,re.sub(self.detailpatt,"_{}".format(idx),hrefs[-2])),self.parse_page)

	def parse_cover(self,response):
		for r in self.parse_bigimg(response):
			yield r
		pages = response.css(".paging_ul a.paging_a_big::text").extract_first()
		hrefs = response.css("a.paging_a_big::attr(href)").extract()
		total = int(pages)

		for idx in xrange(2,total+1):
			yield scrapy.Request(urljoin(response.url,re.sub(self.pattern,"{}".format(idx),hrefs[-1])),self.parse_bigimg)

	def parse_bigimg(self,response):
		for r in self.parse_depage(response):
			yield r
		bigurls = response.css(".c-l_ul .pl_img_box a::attr(href)").extract()
		for bigurl in bigurls:	
			yield scrapy.Request(bigurl,callback=self.parse_page,headers=self.headers)