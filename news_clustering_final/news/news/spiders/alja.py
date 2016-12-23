import scrapy
from news.items import NewsItem
class investigationSpider(scrapy.Spider):
    name = 'jazeera'
    allowed_domains = ['aljazeera.com']
    custom_settings = {
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN":4,
            "BOT_NAME":'inv',
            "DEPTH_LIMIT": 10,
            "USER_AGENT": 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            "REFERER": 'http://www.google.com',
            "COOKIES_ENABLED": False}

#            "DEFAULT_REQUEST_HEADERS":{'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer' : 'http://www.google.com'}
#            }
    def start_requests(self):
        urls = ['http://www.aljazeera.com']
        for url in urls:
            yield scrapy.Request(url=url, callback = self.frontpage, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer' : 'http://www.google.com'})


    def frontpage (self,response):
        url_base = 'http://www.aljazeera.com'
        for link in response.xpath('//div[@id="placeholder1"]//div//@href').extract():
            link = url_base + link
            yield scrapy.Request(url=link, callback = self.read_story, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer' : 'http://www.google.com'}, meta={'ref_url':response.request.url, 'dont_merge_cookies':True})
        for section in response.xpath('//li//@href').extract():
            base_url = 'http://www.aljazeera.com'
            if (section.find('#') == -1) & (section.find('http') == -1):
                section = base_url + section
                yield scrapy.Request(url=section, callback = self.section, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer' : 'http://www.google.com'})


    def read_story(self, response):
        storyItem = NewsItem()
        storyItem['url'] = response.request.url
        storyItem['ref_url'] = response.request.meta['ref_url']
        storyItem['title'] = response.xpath('//h1[@class="heading-story"]//text()').extract()[0]
        story = ""
        try:
            date = response.xpath('//p[@class="meta"]/time/@datetime').extract()[0]
#            date = response.xpath('//time[@class="timestamp"]//text()')[0].extract()
            storyItem['date'] = date
            for i in response.xpath('//div[@id="article-body"]//p')[:-1]:
                for j in  i.xpath('.//text()').extract():
                    stringpart = j.strip()#.replace('\u2019',"'").replace('\u201d',"'").replace('\u201c',"'")
                    story = ''.join([story,' ', stringpart])
            storyItem['text'] = story
        except:
            print "failed"
            storyItem['text'] = ''
            pass
        if len(storyItem['text']) > 1000:
            yield storyItem

        for link in response.xpath('//article//a/@href').extract():
            if (link.find('#') == -1) & (link.find('index.html') == -1) & (link.find('/by/')==-1) & (link.find('news-event') == -1) & (link.find('newsletter') == -1):
                url_base = 'http://www.aljazeera.com'
                link = url_base + link 
                yield scrapy.Request(url=link, callback = self.read_story, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer' : 'http://www.google.com'}, meta={'ref_url':response.request.url, 'dont_merge_cookies':True}) 
    def section(self, response):
        url_base = 'http://www.aljazeera.com'
        try:
            for link in response.xpath('//div[@id="placeholder1"]//div//@href').extract():
                link = url_base + link
                yield scrapy.Request(url=link, callback = self.read_story, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer' : 'http://www.google.com'}, meta={'ref_url':response.request.url, 'dont_merge_cookies':True})
        except:
            pass
