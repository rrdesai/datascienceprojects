import scrapy

class BudgetSpider(scrapy.Spider):
    name = "budget"

    def start_requests(self):
        urls = ['https://www.the-numbers.com/movie/budgets/all']
#        urls = ['http://www.the-numbers.com/movie/Suicide-Squad#tab=summary']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
    def parse(self, response):
        for i in response.xpath('//tr'):
            try:
                reldat = i.xpath('.//td/a/text()').extract()[0]
                title = i.xpath('.//td/b/a/text()').extract()[0]
                rank = i.xpath('.//td[@class="data"]/text()')[0].extract()
                budget = i.xpath('.//td[@class="data"]/text()')[1].extract()
                domestic = i.xpath('.//td[@class="data"]/text()')[2].extract()
                foreign = i.xpath('.//td[@class="data"]/text()')[3].extract()
#                movie_page = i.xpath('.//td/b/a/@href').extract_first()

                yield {'release':reldat.encode('utf-8'), 'title':title.encode('utf-8'),'rank':rank,'budget':budget,'domestic':domestic, 'foreign':foreign}#, 'next':movie_page}
            except: continue
        for i in response.xpath('//tr'):    
            try: movie_page = i.xpath('.//td/b/a/@href').extract_first()    
            except: continue
            if movie_page is not None:
                movie_page = response.urljoin(movie_page)
                yield scrapy.Request(url = movie_page, callback = self.movie)

    def movie(self, response):
        movie_dict = {}
        for i in response.xpath('//div[@id="summary"]//table/tr'):
            try:
                key = i.xpath('.//b/text()').extract()[0].replace(':','').encode('utf-8')
                values = []
                for j in i.xpath('.//a//text()').extract():
                    values.append(j.encode('utf-8'))
                movie_dict[key] = values
            except: continue
        yield movie_dict


