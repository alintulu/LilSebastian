from urllib import request, response, error, parse
from urllib.request import urlopen
from lxml import etree
import numpy as np
import json
import pandas as pd
import pickle

# json file of wanted plants
with open('../input/plants.json') as f:
    want_plants = json.load(f)

# loop and save plant ids
plant_id = []
for p in want_plants:
    plant_id.append(p['id'])

print(plant_id)

# read pickle with information about plants
file = open('../input/scientific_plant_names_appendix_I', 'rb')
scient_plant = pickle.load(file)
file.close()

plant_names = []

# find info about wanted plants from pickle
for i in range(len(scient_plant.index)):
    if scient_plant.iloc[i, 0] in plant_id:
        plant_names.append(scient_plant.iloc[i,9].lower())

print(plant_names)

# json keys
keys_allplants = ['id', 'annotation', 'appendix', 'name']
keys_offers = ['description', 'price', 'min_order', 'link']

def parse(idd, name, tries):

    print("\n!!!!!!!!!!!!!!!!"+name+"!!!!!!!!!!!!!!!!\n")

    # create url for crawler to start search
    temp = name.replace(" ", "+") 
    url="https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={0}&viewtype=G".format(temp)

    # output of crawler
    response = urlopen(url)
    # parser
    htmlparser = etree.HTMLParser()
    # parse and create tree of html
    tree = etree.parse(response, htmlparser)

    xpaths = ['XPATH_PRODUCT_NAME', 'XPATH_PRODUCT_PRICE', 'XPATH_PRODUCT_MIN_ORDER', 'XPATH_PRODUCT_LINK']

    # xpaths of desired info
    XPATH = {
        'XPATH_PRODUCT_NAME' : ".//div[@class='item-info']//h2[contains(@class,'title')]//a/@title",
        'XPATH_PRODUCT_PRICE' : ".//div[@class='item-info']//div[@class='price']/b/text()",
        'XPATH_PRODUCT_MIN_ORDER' : ".//div[@class='item-info']//div[@class='min-order']/b/text()",
        'XPATH_SELLER_YEARS' : ".//div[@class='item-info']//div[@class='stitle util-ellipsis']//div[contains(@class,'supplier-year')]//text()",
        'XPATH_SELLER_NAME' : ".//div[@class='item-info']//div[@class='stitle util-ellipsis']//a/@title", 
        'XPATH_SELLER_RESPONSE_RATE' : ".//div[@class='item-info']//div[@class='sstitle']//div[@class='num']/i/text()",
        'XPATH_PRODUCT_LINK' : ".//div[@class='item-info']//h2/a/@href"
    }

    # check if crawler failed i.e. array is empty
    # if empty, rerun crawler at most 5 times otherwise
    # move on to next plant
    if not tree.xpath(XPATH['XPATH_PRODUCT_NAME']):
        if tries > 4:
            print("failed too many times!!!!!")
        else:
            print("failed but will try again!!!!")
            t = tries + 1
            parse(idd, name, t)
            return

    nr_offers = 0
    # iterate of xpaths and save info
    for key, value in XPATH.items():
        info = tree.xpath(value)
        nr_offers = len(info)
        # fix string
        for i, string in enumerate(info):
            info[i] = string.strip('\n                ')

        print("\n---->", key)
        print(info)

        # save to dict for easy saving into jason
        XPATH[key] = info

    # array of all offers, will contain dict of individual offers
    all_offers = []
    # dict of one offer
    offer = {}
    # iterate over all offers collected by crawler
    for i in range(nr_offers):
        for j, path in enumerate(xpaths):
            if j == 0:
                offer['id'] = i + 1
            try:
                offer[keys_offers[j]] = XPATH[path][i]
            except IndexError:
                offer[keys_offers[j]] = 0
        all_offers.append(offer.copy())

    specific_plant = {}
    specific_plant['id'] = idd
    specific_plant['annotation'] = "1"
    specific_plant['appendix'] = "I"
    specific_plant['name'] = name
    platform = {'platform' : 'alibaba'}
    platform['offers'] = all_offers
    specific_plant['all_offers'] = [platform]

    return specific_plant

# save into json
for i, name in enumerate(plant_names):
    jsonname = '../output/offers.json'
    plant_info = parse(plant_id[i], name, 0)
    if plant_info is None:
        print('ZERO')
    else:
        with open(jsonname, 'a') as outfile:
            json.dump(plant_info, outfile, indent = 4)
