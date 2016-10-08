# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LutherItem(scrapy.Item):
    released = scrapy.Field()
    title = scrapy.Field()
    rank = scrapy.Field()
    budget = scrapy.Field()
    domestic = scrapy.Field()
    worldwide = scrapy.Field()
    critics = scrapy.Field()
    audience = scrapy.Field()
    comps = scrapy.Field()
    franchise = scrapy.Field()
    domesticReleases = scrapy.Field()
    internationalReleases = scrapy.Field()
    mpaaRating = scrapy.Field()
    runtime = scrapy.Field()
    keywords = scrapy.Field()
    source = scrapy.Field()
    genre = scrapy.Field()
    production = scrapy.Field()
    creative = scrapy.Field()
    prodCompanies = scrapy.Field()
    prodCountries = scrapy.Field()
    cast = scrapy.Field()
    crew = scrapy.Field()
    results = scrapy.Field()
    firstdate = scrapy.Field()
    firstviews = scrapy.Field()
    
