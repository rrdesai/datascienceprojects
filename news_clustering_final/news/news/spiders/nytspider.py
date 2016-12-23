import scrapy
from news.items import NewsItem
items = {}
class investigationSpider(scrapy.Spider):
    name = 'times'
    allowed_domains = ['nytimes.com']
    custom_settings = {
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN":4,
            "BOT_NAME":'inv',
            "DEPTH_LIMIT": 10,
            }
    def start_requests(self):
        urls = ['https://www.nytimes.com']
        for url in urls:
            yield scrapy.Request(url=url, callback = self.frontpage)
    def frontpage (self,response):
        for headline in response.xpath('//h2[@class="story-heading"]'):
            try:
                title = headline.xpath('./a/text()').extract()[0]#.strip().replace(u'\u2018','').replace(u'\u2019','')
                link = headline.xpath('./a/@href').extract()[0].strip()
                items[title] = link
            except:
                continue
            if link:
                yield scrapy.Request(url=link, callback = self.read_story)
        for section in response.xpath('//ul[@class="mini-navigation-menu"]//a/@href').extract():
            yield scrapy.Request(url=section, callback = self.section)
    def read_story(self, response):
        storyItem = NewsItem()
        storyItem['url'] = response.request.url
        storyItem['title'] = response.xpath('//h1/text()').extract()[0]
        story = ""
        try:
            date = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()[0]
#            date = response.xpath('//time[@class="dateline"]/text()')[0].extract()
            storyItem['date'] = date
            for i in response.xpath('//body//article[@id="story"]//p[@class="story-body-text story-content"]'):
                for j in  i.xpath('.//text()').extract():
                    stringpart = j.strip()#.replace('\u2019',"'").replace('\u201d',"'").replace('\u201c',"'")
                    story = ''.join([story,' ', stringpart])
            storyItem['text'] = story
        except:
            storyItem['text'] = ''
            pass
        if len(storyItem['text']) > 1000:
            yield storyItem

        for link in response.xpath('//article[@id="story"]//a/@href').extract():
            if (link.find('#') == -1) & (link.find('index.html') == -1) & (link.find('/by/')==-1) & (link.find('news-event') == -1) & (link.find('newsletter') == -1): 
                yield scrapy.Request(url=link, callback = self.read_story) 
        
    def section(self, response):
        if response.xpath('//div[@class="abColumn"]'):
            for i in response.xpath('//div[contains(@class, "columnGroup")]/div[contains(@class, "story") or contains(@class, "ledeStory")]'):
                link = i.xpath('.//a/@href').extract()[0]
                title = i.xpath('.//a/text()').extract()[-1]
                yield scrapy.Request(url=link, callback = self.read_story)
        elif response.xpath('//ol[@class="story-menu"]'):
            for i in response.xpath('//article'):
                link = i.xpath('.//a/@href').extract()[0]
                title = i.xpath('.//a/text()').extract()[-1]
                if title.strip() == '':
                    title = i.xpath('.//h2/text()').extract()[-1]
                yield scrapy.Request(url=link, callback = self.read_story)
