import selenium
from selenium import webdriver as wd
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

from itertools import repeat
import re


url = 'https://www.musinsa.com/app/goods/3471299?loc=goods_rank'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

print(soup.find_all('ul', attrs={'class':'product_article'}))
