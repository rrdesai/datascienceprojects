import scrapy
import re
from luther.items import LutherItem
class BudgetSpider(scrapy.Spider):
    name = "itspy"
    items = []
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
        }
    def start_requests(self):
        urls = ['https://www.the-numbers.com/movie/budgets/all']
#        urls = ['http://www.the-numbers.com/movie/Suicide-Squad#tab=summary']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
    def parse(self, response):
        for i in response.xpath('//tr'):
            movie_item = LutherItem()
            try:
                reldat = i.xpath('.//td/a/text()').extract()[0]
                title = i.xpath('.//td/b/a/text()').extract()[0]
                rank = i.xpath('.//td[@class="data"]/text()')[0].extract()
                budget = i.xpath('.//td[@class="data"]/text()')[1].extract()
                domestic = i.xpath('.//td[@class="data"]/text()')[2].extract()
                foreign = i.xpath('.//td[@class="data"]/text()')[3].extract()
#                movie_page = i.xpath('.//td/b/a/@href').extract_first()
                movie_item['released'] = reldat
                movie_item['title'] = title
                movie_item['rank'] = rank
                movie_item['budget'] = budget
                movie_item['domestic'] = domestic
                movie_item['worldwide'] = foreign
            except: continue
            try: movie_page = i.xpath('.//td/b/a/@href').extract_first()    
            except: continue
            if movie_page is not None:
                movie_page = response.urljoin(movie_page)
                yield scrapy.Request(url = movie_page,meta={'item':movie_item}, callback = self.movie)
            
    def movie(self, response):
        movie = {}
        for i in response.xpath('//div[@id="summary"]//table/tr'):
            try:
                key = i.xpath('.//b/text()').extract()[0].replace(':','').encode('utf-8')
                values = []
                for j in i.xpath('.//a//text()').extract():
                    values.append(j.encode('utf-8'))
                movie[key] = values
            except: continue
        cast = {}
        crew = {}
        for i in response.xpath('//div[@id="cast"]'):
            if i.xpath('.//h1/text()').extract()[0] == 'Cast':                          
                key = i.xpath('.//td[@class="alnleft"]//text()').extract()
                value = i.xpath('.//td[@class="alnright"]//text()').extract()
                for j in range(len(key)):
                    cast[key[j]] = value[j]
            
            elif i.xpath('.//h1/text()').extract()[0] == 'Production and Technical Credits':
                key = i.xpath('.//td[@class="alnleft"]//text()').extract()
                value = i.xpath('.//td[@class="alnright"]//text()').extract()
                for j in range(len(key)):
                    crew[key[j]] = value[j]
                    
        tofix = movie
        movie = {}
        for i in tofix.keys():
            movie[i.replace('\xc2\xa0', ' ')] = tofix[i]
#        yield movie    
        item = response.request.meta['item']
        try:
            item['critics'] = movie['Critics'][2]
        except: pass
        try:
            item['audience'] = movie['Critics'][5]
        except: pass
        try:
            item['comps'] = movie['Comparisons'][:-1]
        except: pass
        try:
            item['domesticReleases']= movie['Domestic Releases']
        except: pass
        try:
            item['internationalReleases']= movie['International Releases']
        except: pass
        try:
            item['mpaaRating'] = movie['MPAA Rating']
        except: pass
        try:
            item['franchise'] = movie['Franchise']
        except: pass
        try:
            item['runtime'] = movie['Running Time']
        except: pass
        try:
            item['keywords'] = movie['Keywords']
        except: pass
        try:
            item['source'] = movie['Source']
        except: pass
        try:
            item['genre'] = movie['Genre']
        except: pass
        try:
            item['production'] = movie['Production Method']
        except: pass
        try:
            item['creative'] = movie['Creative Type']
        except: pass
        try:
            item['prodCompanies'] = movie['Production Companies']
        except: pass
        try:
            item['prodCountries'] = movie['Production Countries']
        except: pass
        try:
            item['cast'] = cast
        except: pass
        try:
            item['crew'] = crew
        except: pass
        base_url = 'https://www.youtube.com/results?search_query={}'
        if re.search("(\\\)",item['title']):
            yield item
        else:
            url = 'https://www.youtube.com/results?search_query={}+Trailer'
            title = '+'.join(re.findall("(\w+)",item['title']))
            url = url.format(title)
            yield scrapy.Request(url=url, meta = {'item':item}, callback = self.youtube)

    def youtube(self, response):
        item = response.request.meta['item']
        try:
            item['results'] =  response.xpath('//p[@class="num-results first-focus"]//text()').extract_first().split(' ')[1]
            item['firstdate'] = response.xpath('//ul[@class="yt-lockup-meta-info"]//text()')[0].extract()
            item['firstviews'] = response.xpath('//ul[@class="yt-lockup-meta-info"]//text()')[1].extract()
            yield item
        except:
            yield item
