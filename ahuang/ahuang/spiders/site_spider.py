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
    	"DOWNLOAD_DELAY": 1,
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


class SiteShadowpider(scrapy.Spider):

	name = "shadow"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }

	start_urls=["https://doub.io/sszhfx/"]

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url,self.parse_page)

	def parse_page(self,response):
		imgs = response.css(".article-content a.dl1::attr(href)").extract()
		for img in imgs:
			yield ImageItem(url=img,created=datetime.now(),source=response.url)

	
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
	

class SiteBaiduTextSpider(scrapy.Spider):

	name = "baidu"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Cookie':'BDIMGISLOGIN=0; BDqhfp=%E4%BA%8C%E7%BB%B4%E7%A0%81%26%260-10-1undefined%26%260%26%261; BAIDUID=CF7EDFAB88B351DDECCFD0E3501FFBC0:FG=1; BIDUPSID=CF7EDFAB88B351DDECCFD0E3501FFBC0; PSTM=1497495738; pgv_pvi=7128611840; pgv_si=s2617850880; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[tox4WRQ4-Km]=mk3SLVN4HKm; PSINO=7; H_PS_PSSID=23201_1469_21110_17001_20927; firstShowTip=1; userFrom=null',
		'Referer':'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1497510737258_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E4%BA%8C%E7%BB%B4%E7%A0%81'
		}
	
	base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%9D%A1%E5%BD%A2%E7%A0%81&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%E6%9D%A1%E5%BD%A2%E7%A0%81&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn={}&rn=30&gsm=1e&1497585992846="
	
	def start_requests(self):
		for idx in xrange(1,41):
			yield scrapy.Request(self.base_url.format(30*idx),self.parse_images)
	
	def parse_images(self,response):
		info = json.loads(response.body_as_unicode())
		data = info["data"]
		for item in data:
			objURL = item.get("objURL")
			if objURL:
				url = uncompile_url(objURL)
				yield ImageItem(url=url,created=datetime.now())


class SiteJuzimiSpider(scrapy.Spider):

	name = "juzimi"
	CUSTOM_SETTINGS = {
    	"DOWNLOAD_DELAY": 1,
    	"CONCURRENT_REQUESTS_PER_DOMAIN": 20
	}
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }
       
	base_url = "http://www.juzimi.com/meitumeiju/shouxiemeiju?page={}"


	def start_requests(self):
		for idx in xrange(1,31):
			yield scrapy.Request(self.base_url.format(idx),self.parse_page)

	def parse_page(self,response):
		imgs = response.css(".chromeimg::attr(src)").extract()
		for img in imgs:
			yield ImageItem(url=urljoin("http:",img),created=datetime.now(),source=response.url)

