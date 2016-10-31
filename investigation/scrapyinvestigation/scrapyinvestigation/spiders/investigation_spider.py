import scrapy
items = {}
class investigationSpider(scrapy.Spider):
    name = 'investigation'
    custom_settings = {
            "DOWNLOAD_DELAY": 5,
            "CONCURRENT_REQUESTS_PER_DOMAIN":2,
            "BOT_NAME":'inv',
            #            "USER_AGENT":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
            }
    def start_requests(self):
        urls = ['https://www.nytimes.com']
        for url in urls:
            yield scrapy.Request(url=url, callback = self.frontpage)
    def frontpage(self,response):
        for headline in response.xpath('//h2[@class="story-heading"]'):
            try:
                title = headline.xpath('./a/text()').extract()[0].strip().replace(u'\u2018','').replace(u'\u2019','')
                link = headline.xpath('./a/@href').extract()[0].strip()
                items[title] = link
            except:
                continue
        return items
