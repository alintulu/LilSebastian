from urllib import request, response, error, parse
from urllib.request import urlopen
from lxml import etree
import numpy as np
import json
import pandas as pd

# json keys
keys_allplants = ['id', 'annotation', 'appendix', 'name']#, 'nonscientific name']
keys_offers = ['description', 'price', 'min_order', 'link']
value = ['18189', '1', 'I', 'ariocarpus retusus']

df = pd.DataFrame(columns = keys_allplants)
df.loc[0] = value

# name = 'plant and seed oils'
#url = 'https://www.alibaba.com/catalog/plant-animal-oil_cid136?spm=a2700.8270666-1.left-category.5.71a74cc2ZkXTvG'
# name = 'plant seed and bulbs'
#url ='https://www.alibaba.com/catalog/plant-seeds-bulbs_cid100001746?spm=a2700.8270666-1.left-category.33.71a74cc2ZkXTvGi'
#url = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=ariocarpus+retusus&viewtype=G&tab='
name = 'ariocarpus retusus'
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

# array of all offers, will contain dict of one offer
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
platform = {'platform' : 'ebay'}
for index, row in df.iterrows():
    for i, key in enumerate(keys_allplants):
        specific_plant[key] = row[key]
    platform['offers'] = all_offers
    specific_plant['all_offers'] = platform

# save into json
name = '../output/'+name.replace(" ", "")+'.json'
with open(name) as f:
    test = json.load(f)
    print(type(test))

with open(name, 'w') as outfile:
    json.dump([specific_plant], outfile, indent = 4)
