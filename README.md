# Team Li'l Sebastian for Zoohackathon 2019 Helsinki

## Our contribution to problem 6

This is a web scraper as part of our application for Zoohackathon 2019 in Helsinki. You can find the full application and further information at [https://devpost.com/software/li-l-sebastian](https://devpost.com/software/li-l-sebastian). 

## How it works

  - The json file [input/plants.json](https://github.com/alintulu/LilSebastian/blob/master/input/plants.json) contains the names and ids of the CITES listed plants we would like to find further information on
  - The python file [crawler/final_crawler.py](https://github.com/alintulu/LilSebastian/blob/master/crawler/final_crawler.py) is my final version of the crawler I use to scrape with
  - Run it by being in the folder `crawler` an type into the terminal
  
  ```
  python final_crawler.py
  ```

## What it does

To help reduce the overall demand of trafficked plants, this tool helps to identify sellers and offers of CITES listed plant species through popular e-commerce sites, to reduce the amount of manual labour on the part of law enforcement individuals and CITES staff.

## How we built it

We used a scraper to identify the relevant postings on alibaba, which then fed into a json file. The data was then used to populate the Progressive Web App (PWA) built with ReactJS.

## Python requirements

  - urllib
  - lxml
  - pandas
  - json
  - pickle 


