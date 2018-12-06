import scrapy
import json
from scrapy.http import FormRequest
from scrapy.http.headers import Headers
from urllib import urlencode
from scrapy import Request
from scrapy.http.cookies import CookieJar
import re
class BlogSpider(scrapy.Spider):
	name = "news"
	def __init__(self, *args, **kwargs):
		super(BlogSpider, self).__init__(*args, **kwargs)
		self.start_urls = ['http://www.alazraq.com']
	def parse(self, response):
		i=0
		for news in response.css('a'):
			next_page = news.css('a::attr("href")').extract_first()
			print("-----------------------------------")
			if next_page:
				yield scrapy.Request(response.urljoin(next_page),callback=self.news_details)
	def news_details(self, response):
		href = response.url
		details = response.css('.article_content_title ::text').extract_first()
		article_title = response.css('.article_title ::text').extract_first()
		date = response.css('.Main_article_date ::text').extract_first()
		
		print(details)
		print(article_title)
		print(date)
		yield {"details":details,"href":href,"article_title":article_title,"date":date}