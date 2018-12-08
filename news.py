# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import FormRequest
from scrapy.http.headers import Headers
from urllib import urlencode
from scrapy import Request
from scrapy.http.cookies import CookieJar
import re
import urlparse
class BlogSpider(scrapy.Spider):
	name = "news"
	def __init__(self, *args, **kwargs):
		super(BlogSpider, self).__init__(*args, **kwargs)
		self.start_urls = ['http://www.alazraq.com']
	def parse(self, response):
		for news in response.css('.category'):
			next_page = news.css('a::attr("href")').extract_first()
			if next_page:
				yield scrapy.Request(response.urljoin(next_page),callback=self.get_pages)
	def get_pages(self,response):
		href = response.url
		page = response.css('td:nth-child(3) font.Category ::text').extract_first()
		page = page.replace(u'من','')
		page = page.replace(u'صفحة ','')
		page = page.replace(u'\u0627\u0644\n\xa01\xa0\n\n\xa0','')
		for i in range(1,(int(page)+1)):
			page_href = href+"&screen="+str(i)
			yield scrapy.Request(response.urljoin(page_href),callback=self.category_list)
	def category_list(self,response):
		href = response.url		
		for news in response.css('.More_News_titles'):
			next_page = news.css('a::attr("href")').extract_first()
			par = urlparse.parse_qs(urlparse.urlparse(url).query)
			news_id = (par['a_id'][0])
			print(news_id)
			if next_page:
				yield scrapy.Request(response.urljoin(next_page),callback=self.news_details)
		print(href)
	def news_details(self, response):
		import sys
		reload(sys)
		sys.setdefaultencoding('utf-8')
		href = response.url
		details = response.css('.article_content_title ::text').extract()
		article_title = response.css('.article_title ::text').extract_first()
		date = response.css('.Main_article_date ::text').extract_first()
		
		print(details)
		print(article_title)
		print(date)
		yield {"details":json.dumps(details,ensure_ascii=False).encode('utf8'),"href":href,"article_title":article_title,"date":date}