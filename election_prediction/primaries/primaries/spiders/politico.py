import scrapy
from primaries.items import PrimariesItem
import time
from selenium import selenium
from selenium import webdriver
from scrapy.http.request import Request
from selenium.webdriver.common.keys import Keys
import os

states_dict = {}
chromedriver = "/Users/R1/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

class politico(scrapy.Spider):
    name = "prispy"
    custom_settings = {
            "DOWNLOAD_DELAY" : 2,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 2
            }
  
    def __init__(self):
        self.driver = webdriver.Chrome(chromedriver)
        scrapy.Spider.__init__(self)

    def __del__(self):
        scrapy.Spider.__del__(self)

    def start_requests(self):
        url_base = "http://www.politico.com/2016-election/primary/results/map/president/{}/"
        states = ['louisiana']
#        states = ['alabama','alaska','arizona','arkansas','california','colorado','connecticut','delaware','florida','georgia','hawaii','idaho','illinois','indiana','iowa','kansas','kentucky','louisiana','maine','maryland','massachusetts','michigan','minnesota','mississippi','missouri','montana','nebraska','nevada','new-hampshire','new-jersey','new-mexico','new-york','north-carolina','north-dakota','ohio','oklahoma','oregon','pennsylvania','rhode-island','south-carolina','south-dakota','tennessee','texas','utah','vermont','virginia','washington','west-virginia','wisconsin','wyoming','district-of-columbia']

        for i in states:
            url = url_base.format(i)
            yield scrapy.Request(url = url, callback = self.parse)
    
    def parse(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0,99999999999999);")
        time.sleep(10)
        state = response.url.split('/')[-2]
        counties = {}
        for i in self.driver.find_elements_by_xpath('//article[@class = "results-group"]'):
            try:
                county = i.find_element_by_xpath('./header/div/h4').text
            except:
                print "no counties found"
                continue
            candidates = {}
            for j in i.find_elements_by_xpath('./div[@class = "results-dataset"]//table[@class ="results-table"]//tr'):
                try:
                    candidate = j.find_element_by_xpath('.//span[@class = "name-combo"]').text
                    percent = j.find_element_by_xpath('.//span[@class = "percentage-combo"]').text
                    votes = j.find_element_by_xpath('.//td[@class = "results-popular"]').text
                    candidates[candidate] = (percent,votes)
                except: continue
            counties[county] = candidates
        states_dict[state] = counties
        return states_dict
#        if len(states_dict.keys()) >= 49:
#            return states_dict
#        print counties
#    states_dict[state] = counties
#    print 'states',states_dict
#        for i in response.xpath('//article[@class="results-group"]'):
#            try:
#                county = i.xpath('./header/div/h4/text()').extract()[0]
#            except:
#                print "no counties found"
#                print state
#                continue
#            candidates = {}
#            for j in i.xpath('./div[@class="results-dataset"]//table[@class="results-table"]//tr'):
#                candidate = j.xpath('.//span[@class ="name-combo"]/text()').extract()[0]
#                percent = j.xpath('.//span[@class = "percentage-combo"]/span[@class="number"]/text()').extract()[0]
#                votes = j.xpath('.//td[@class = "results-popular"]/text()').extract()[0]
#                candidates[candidate] = (percent, votes)
#            counties[county] = candidates
#        states_dict[state] = counties
#        return states_dict
