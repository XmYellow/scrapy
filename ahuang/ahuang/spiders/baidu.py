import scrapy
from ..items import ImageItem
from datetime import datetime
from urlparse import urljoin
import re 
import json
from escape import uncompile_url


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
		for idx in xrange(1,2):
			yield scrapy.Request(self.base_url.format(30*idx),self.parse_images)
	
	def parse_images(self,response):
		info = json.loads(response.body_as_unicode())
		data = info["data"]
		for item in data:
			objURL = item.get("objURL")
			if objURL:
				url = uncompile_url(objURL)
				yield ImageItem(url=url,created=datetime.now())

