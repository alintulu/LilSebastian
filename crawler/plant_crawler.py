from urllib import request, response, error, parse
from urllib.request import urlopen
from lxml import etree
import numpy as np
import json

# name = 'plant and seed oils'
#url = 'https://www.alibaba.com/catalog/plant-animal-oil_cid136?spm=a2700.8270666-1.left-category.5.71a74cc2ZkXTvG'
# name = 'plant seed and bulbs'
#url ='https://www.alibaba.com/catalog/plant-seeds-bulbs_cid100001746?spm=a2700.8270666-1.left-category.33.71a74cc2ZkXTvGi'
name = 'ariocarpus retusus'
url = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=ariocarpus+retusus&viewtype=G&tab='

# output of crawler
response = urlopen(url)
# parser
htmlparser = etree.HTMLParser()
# parse and create tree of html
tree = etree.parse(response, htmlparser)

# xpaths of desired info
XPATH = {
    'XPATH_PRODUCT_NAME' : ".//div[@class='item-info']//h2[contains(@class,'title')]//a/@title",
    'XPATH_PRODUCT_PRICE' : ".//div[@class='item-info']//div[@class='price']/b/text()",
    'XPATH_PRODUCT_MIN_ORDER' : ".//div[@class='item-info']//div[@class='min-order']/b/text()",
    'XPATH_SELLER_YEARS' : ".//div[@class='item-info']//div[@class='stitle util-ellipsis']//div[contains(@class,'supplier-year')]//text()",
    'XPATH_SELLER_NAME' : ".//div[@class='item-info']//div[@class='stitle util-ellipsis']//a/@title", 
    'XPATH_PRODUCT_LINK' : ".//div[@class='item-info']//h2/a/@href"
}

# iterate of xpaths and save info
for key, value in XPATH.items():
    info = tree.xpath(value)
    # fix string
    for i, string in enumerate(info):
        info[i] = string.strip('\n                ')

    print("\n---->", key)
    print(info)

    # save to dict for easy saving into jason
    XPATH[key] = info

# save into json
name = '../output/'+name.replace(" ", "")+'.json'
with open(name, 'w') as outfile:
    json.dump(XPATH, outfile)
