import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url

	
class SiteOumopider(scrapy.Spider):

	name = "oumo"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 5,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 5
	}
	headers = {
        'Referer':'https://www.om.cn/product/0-17-2-0-1-17-170-0-2-2-0',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

	start_urls=["https://a.om.cn/api/models/search/l-1-17-170-0-2-2-0-40"]


	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url,self.parse_page)

	def parse_page(self,response):
		info = json.loads(response.body_as_unicode())
		nextpage = info["next_page_url"]
		data = info["data"]
		for item in data:
			idx = str(item["id"])
			url = 'https://a.om.cn/api/models/details/'+idx
			yield scrapy.Request(url,self.parse_detail)
		nexturl = urljoin(response.url,nextpage,self.start_urls[0])
		if nextpage == 'l-1-17-170-2-2-2-0-40':
			return
		yield scrapy.Request(nexturl,self.parse_page)	

	def parse_detail(self,response):
		urls = json.loads(response.body_as_unicode())
		imgurls = urls["atlas"]
		url = json.loads(imgurls)
		for img in url:
			imgurl = urljoin('https://v3download.om.cn/',img),
			yield ImageItem(url=imgurl,created=datetime.now())