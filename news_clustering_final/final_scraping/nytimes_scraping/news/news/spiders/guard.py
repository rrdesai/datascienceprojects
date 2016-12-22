import scrapy
from news.items import NewsItem
class investigationSpider(scrapy.Spider):
    name = 'guard'
    allowed_domains = ['theguardian.com']
    custom_settings = {
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN":4,
            "BOT_NAME":'inv',
            "DEPTH_LIMIT": 10,
            }
    def start_requests(self):
        urls = ['http://www.theguardian.com']
        for url in urls:
            yield scrapy.Request(url=url, callback = self.frontpage)
    def frontpage (self,response):
        for headline in response.xpath('//section//li[contains(@class, "fc-slice__item")]'):
            try:
                link = headline.xpath('.//@href').extract()[0].strip()
            except:
                continue
            if link:
                yield scrapy.Request(url=link, callback = self.read_story)
        for section in response.xpath('//li[@class="top-navigation__item"]').extract():
            yield scrapy.Request(url=section, callback = self.section)
    def read_story(self, response):
        storyItem = NewsItem()
        storyItem['url'] = response.request.url
        story = ""
        try:
            date = response.xpath('//time[@itemprop="datePublished"]/@datetime').extract()[0]
            storyItem['date'] = date
            storyItem['title'] = response.xpath('//h1/text()').extract()[0]
            for i in response.xpath('//div[contains(@class, "content__article-body")]//p'):
                for j in  i.xpath('.//text()').extract():
                    stringpart = j.strip()#.replace('\u2019',"'").replace('\u201d',"'").replace('\u201c',"'")
                    story = ''.join([story,' ', stringpart])
            storyItem['text'] = story
        except:
            storyItem['text'] = ''
            pass
        if len(storyItem['text']) > 1000:
            yield storyItem


        for link in response.xpath('//div[contains(@class, "content__article-body")]//a/@href').extract():
            if (link.find('#') == -1) & (link.find('index.html') == -1) & (link.find('/by/')==-1) & (link.find('news-event') == -1) & (link.find('newsletter') == -1): 
                yield scrapy.Request(url=link, callback = self.read_story) 
        
    def section(self, response):
        for headline in response.xpath('//section//li[contains(@class, "fc-slice__item")]'):
            try:
                link = headline.xpath('.//@href').extract()[0].strip()
            except:
                continue
            if link:
                yield scrapy.Request(url=link, callback = self.read_story)
