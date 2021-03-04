import scrapy

from scrapy.loader import ItemLoader
from ..items import BbvaItem
from itemloaders.processors import TakeFirst


class BbvaSpider(scrapy.Spider):
	name = 'bbva'
	start_urls = ['https://www.bbva.com/en/latest-news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="noticia_InfoHeader"]/h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="article-title"]/text()').get()
		description = response.xpath('//div[@class="detContIntro" or @class="detContText"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="detAreaDate rs_skip"]/span/text()').get()

		item = ItemLoader(item=BbvaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
