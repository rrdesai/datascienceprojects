import json
import numpy as np
import gc
import pandas as pd
import sys
from copy import copy
from mitie import *
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer




sys.path.append('~/mitie')
ner = named_entity_extractor('../../../mitie/mitie-v0.2-python-2.7-windows-or-linux64/MITIE-models/english/ner_model.dat')
pd.options.display.max_colwidth = 250
pd.options.display.max_rows = 400
lemmatizer = WordNetLemmatizer()
vocabdict = defaultdict(int)
entities_dict = defaultdict(int)

def lemmatize_me(x):
    try:
        x_tagged = pos_tag(x)
    except:
        return 'failed'
    return_list = []
    for i in x_tagged:
        if 'V' in i[1]:
            value = 'v'
        else:
            value = 'n'
        return_list.append(lemmatizer.lemmatize(i[0], pos = value))
    return ' '.join(return_list)


def remove_blanks(x):
    x_lis = x
    while True:
        try:
            x_lis.remove('')
        except:
            return x_lis


def date_conv(x):
    x = x.strip().replace(u'\xa0',' ').encode('utf-8')
    split = x.split('T')
    if (x.find('T') != len(x) - 1) or (x.find('T') == -1) :
        return pd.to_datetime(split[0], format='%Y-%m-%d')
    else:
        split = x.split(' ')
        date = '-'.join(split[:3])
        return pd.to_datetime(date, format='%d-%b-%Y')


def get_ent_simp(x, dictname=entities_dict):
        x = tokenize(x)
        entities = ner.extract_entities(x)
        for e in entities:
            rangee = e[0]
            entity_text = " ".join(x[i] for i in rangee)
            dictname[entity_text]+=1
        

def len_filter(x):
    ret_list = []
    for i in x:
        if len(i) > 3:
            ret_list.append(i)
    return ret_list


def clean_text(x):
    val = x.encode('utf-8').replace("\xe2\x80\x99","'").replace("\xe2\x80\x9c",'"').replace("\xe2\x80\x9d",'"').replace('\xe2\x80\x94',"'").replace('\xe2\x80\xa6','...')
    return val



