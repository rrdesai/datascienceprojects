import scrapy
import time
from selenium import selenium
from selenium import webdriver
from scrapy.http.request import Request
from selenium.webdriver.common.keys import Keys
import os

states_dict = {}
chromedriver = "/Users/R1/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

class cnn(scrapy.Spider):
    name = "lastprim"
    custom_settings = {
            "DOWNLOAD_DELAY":2,
            "CONCURRENT_REQUESTS_PER_DOMAIN":1
            }
    def __init__(self):
        self.driver = webdriver.Chrome(chromedriver)
        scrapy.Spider.__init__(self)
    def __del__(self):
        scrapy.Spider.__del__(self)

    def start_requests(self):
        url_base = "http://www.cnn.com/ELECTION/2008/primaries/results/county/#val={}PRIMARY1"
        states = ['MS','AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC']
        parties = ['REP','DEM']
        start_urls = []
        for i in states:
            for j in parties:
                start_urls.append(i+j)

        for i in start_urls:
            url = url_base.format(i)
            yield scrapy.Request(url = url, callback = self.parse, dont_filter=True)

    def parse(self, response):
        self.driver.get(response.request.url)
        self.driver.get(response.request.url)
        time.sleep(6)
        state = self.driver.find_element_by_xpath('//div[@class="cnnElexPrimC_head"]//a').text
        if state in states_dict.keys():
            exists = True
        else:
            exists = False
        counties = {}
        new_pages = True
        checknext = False
        while new_pages == True:
            for i in self.driver.find_elements_by_xpath('//div[@class="cnnElexPrimCountyTable"]//tr'):
                if len(self.driver.find_elements_by_xpath('.//td')) < 2:
                    print "not long enough, skipping"
                    continue
                try:
                    county = i.find_element_by_xpath('.//div[@class="state_name"]/b').text
                    if exists == False:
                        counties[county] = {}
                except:
                    next
                try:
                    try:
                        candidate = i.find_element_by_xpath('.//td[@class="cand bord_b"]//b').text
                        votes = i.find_element_by_xpath('.//td[@class="bord_b"]/div[@class="pad"]').text
                        percent = i.find_element_by_xpath('.//td[@class="bord_b"]/div[@class="pad"]/b').text[:-1]
                    except: 
                        candidate = i.find_element_by_xpath('.//td[@class="cand "]//b').text
                        votes = i.find_element_by_xpath('.//td[@class!="cand "]/div[@class="pad"]').text
                        percent = i.find_element_by_xpath('.//td/div[@class="pad"]/b').text[:-1]
                    finally:
                        if exists == False:
                            counties[county][candidate] =(votes,percent)
                        else:
                            states_dict[state][county][candidate] = (votes,percent)
                except:
                    continue
            elements = self.driver.find_elements_by_xpath('//div[@id="cnnElexRBCounty_right"]/table//tr//a')
            if len(elements) <2:
                if checknext == True:
                    print "no more pages"
                    new_pages = False
                else:
                    checknext = True

            try:
                elements[-1].click()
                time.sleep(2)
            except:
                continue
        if exists == False:
            states_dict[state] = counties
        if len(states_dict.keys()) >49: return states_dict
