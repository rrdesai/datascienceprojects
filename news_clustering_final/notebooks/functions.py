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


def get_people(x):
        x = tokenize(x)
        entities = ner.extract_entities(x)
        ent_list = []
        for e in entities:
            if (e[1]=='PERSON') & (len(e[0])>1) & (e[2] > 1) :
                
                rangee = e[0]
                entity_text = " ".join(x[i] for i in rangee)
#                 print e[2],' ',entity_text
                entity_text.decode("utf-8").encode("ascii","ignore")
                ent_list.append(entity_text)
        return(list(set(ent_list)))


def trim_data(x):
    if len(focus_vocab) <= 5:
        if len(set(x).intersection(set(focus_vocab))) == len(focus_vocab):
            return 1
    elif len(set(x).intersection(set(focus_vocab))) >  round(len(focus_vocab)*0.6):
            return 1
    else:
           return 0

def get_locations(x):
        x = tokenize(x)
        entities = ner.extract_entities(x)
        ent_list = []
        for e in entities:
            if (e[1]=='LOCATION') & (e[2] >1) :
                
                rangee = e[0]
                entity_text = " ".join(x[i] for i in rangee)
#                 print e[2],' ',entity_text
                entity_text.decode("utf-8").encode("ascii","ignore")
                ent_list.append(entity_text)
        return(list(set(ent_list)))

def get_orgs(x):
        x = tokenize(x)
        entities = ner.extract_entities(x)
        ent_list = []
        for e in entities:
            if (e[1]=='ORGANIZATION') & (e[2] >1) :
                
                rangee = e[0]
                entity_text = " ".join(x[i] for i in rangee)
#                 print e[2],' ',entity_text
                entity_text.decode("utf-8").encode("ascii","ignore")
                ent_list.append(entity_text)
        return(list(set(ent_list)))

"""
Average distance calculator for spectral clustering in scikit learn
adapted from vizualization scripts by David Andrzejewski
"""
import numpy as NP
import matplotlib.pyplot as P
import matplotlib.lines as L
import sklearn.cluster as SKLC

# from scaledimage import scaledimage

def blockviz(affinity, nclust, ax=None):


    # Do spectral clustering
    ndata = affinity.shape[0]
    c = SKLC.SpectralClustering(n_clusters=nclust, affinity='linear', random_state=1445)
    c.fit(affinity)
    # Extract cluster labels and sort indices to align with clusters
    sortidx = []
    for ki in range(nclust):
        sortidx += getlabeled(c.labels_, ki)
    sorted_affinity = affinity.copy()
    sorted_affinity = sorted_affinity[sortidx,:]
    sorted_affinity = sorted_affinity[:,sortidx]
    kstart = 0
    clus_size = []
    clus_start = []
    for ki in range(nclust):    
        clustki = getlabeled(c.labels_, ki)
        clus_size.append(clustki)
        kstart += len(clustki)
        clus_start.append(kstart)
    return clus_size,clus_start, sorted_affinity,c.labels_

def logistic(val):
    """ Logistic function """
    return float(1) / (1 + NP.exp(-1 * val))

def getlabeled(labels, ki):
    """ Get indices where labels==ki """
    return [idx for (idx, val) in 
            enumerate(labels) if val == ki]

def drawH(ax, y, xstart, xend):
    """ Draw horiztonal line """
    ax.add_line(L.Line2D([xstart, xend], 
                  [y, y],
                  color='r'))

def drawV(ax, x, ystart, yend):
    """ Draw vertical line """
    ax.add_line(L.Line2D([x, x],
                         [ystart, yend], 
                         color='r'))

def drawClust(ax, kstart, kend, kmax, scale=1):
    """ Draw bounding box for cluster """
    skstart = scale * kstart
    skend = scale * kend
    skmax = scale * kmax
    if(skstart == 0):
        # Upper-left cluster: only draw bottom-right borders
        drawH(ax, skmax-skend, skstart, skend)
        drawV(ax, skend, skmax-skstart, skmax-skend)
    elif(skend == skmax):
        # Lower-right cluster: only draw top-left borders
        drawH(ax, skmax-skstart, skstart, skend)
        drawV(ax, skstart, skmax-skstart, skmax-skend)
    else:
        # Otherwise, draw all 4 borders
        drawH(ax, skmax-skend, skstart, skend)
        drawV(ax, skend, skmax-skstart, skmax-skend)
        drawH(ax, skmax-skstart, skstart, skend)
        drawV(ax, skstart, skmax-skstart, skmax-skend)
        
import numpy as NP
import matplotlib.pyplot as P
import matplotlib.ticker as MT
import matplotlib.cm as CM
 
def scaledimage(W, pixwidth=20, ax=None, grayscale=True):
    """
    Do intensity plot, similar to MATLAB imagesc()
 
    W = intensity matrix to visualize
    pixwidth = size of each W element
    ax = matplotlib Axes to draw on 
    grayscale = use grayscale color map
 
    Rely on caller to .show()
    """
    # N = rows, M = column
    (N, M) = W.shape 
    # Need to create a new Axes?
    if(ax == None):
        ax = P.figure(figsize=(20,20)).gca()
    # extents = Left Right Bottom Top
    exts = (0, pixwidth * M, 0, pixwidth * N)
    if(grayscale):
        ax.imshow(W,
                  interpolation='nearest',
                  cmap=CM.gray,
                  extent=exts)
    else:
        ax.imshow(W,
                  interpolation='nearest',
                  extent=exts)
 
    ax.xaxis.set_major_locator(MT.NullLocator())
    ax.yaxis.set_major_locator(MT.NullLocator())
    return ax
 
if __name__ == '__main__':
    # Define a synthetic test dataset
     testweights = NP.array([[0.25, 0.50, 0.25, 0.00],
                            [0.00, 0.50, 0.00, 0.00],
                            [0.00, 0.10, 0.10, 0.00],
                            [0.00, 0.00, 0.25, 0.75]])
    # Display it
#     ax = scaledimage(testweights)
#     P.show()