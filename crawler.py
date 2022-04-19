import pandas as pd
import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 擷取網站
def yahoo(item):
    print('===== yahoo =====')
    url = f'https://tw.buy.yahoo.com/search/product?p={item}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())

    # 整理資料
    # 1.擷取批次網址
    items = soup.find('div',class_='main').find('ul',class_='gridList').findAll('li',class_='BaseGridItem__grid___2wuJ7')

    links = []
    for i in items:
        links.append(i.find('a')['href'])
    #print(links)

    # 2.彙整批次  網址   商品名稱   價格   圖片
    products = []
    for link in links:
        r = requests.get(link)
        response = r.text
        soup2 = BeautifulSoup(response)
        product = {}
        product['網址'] = link
        product['商品名稱'] = soup2.find('h1', class_='HeroInfo__title___57Yfg HeroInfo__textTooLong___BXk8j').text
        product['價格'] = soup2.find('div', class_='HeroInfo__mainPrice___1xP9H').text
        product['圖片'] = soup2.find('img', class_='LensImage__img___3khRA')['src']
        products.append(product)
    # print(products, len(products))

    # 建立資料表
    df1 = pd.DataFrame(products)
    df1['來源'] = 'Yahoo'
    df1['建立時間'] = datetime.today()
    # print(df1)

    return df1


def momo(item):
    print('===== momo =====')
    # headless 瀏覽器 = 無介面板的瀏覽器
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # 啟用模擬器
    # browser = webdriver.Chrome(executable_path='./chromedriver')
    browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)

    url = f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={item}&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType'

    # 模擬開啟網頁
    browser.get(url)

    # 模擬網頁下拉
    for y in range(0, 10000, 500):
       browser.execute_script(f"window.scrollTo(0, {y})")
       time.sleep(0.5)

    # 擷取網頁原始碼
    source = browser.page_source

    # 關閉模擬瀏覽器
    browser.quit()

    soup = BeautifulSoup(source)
    # print(soup.prettify())

    # 整理資料
    products = []
    for i in soup.find('div',class_="listArea").ul.find_all('li'):
        product = {}
        # 網址
        product['網址'] = 'https://www.momoshop.com.tw/'+i.find('a',class_="goodsUrl")['href']
        # print('https://www.momoshop.com.tw/'+i.find('a',class_="goodsUrl")['href'])
        # 品名
        product['商品名稱'] = i.find('h3',class_="prdName").text
        # print(i.find('h3',class_="prdName").text)
        # 價格
        product['價格'] = i.find('span',class_="price").text
        # print(i.find('span',class_="price").text)
        # 圖片
        product['圖片'] = i.find('img', class_="prdImg lazy lazy-loaded")['src']
        # print(i.find('img')['src'])
        products.append(product)
    # print(products, len(products))

    # 建立資料表
    df2 = pd.DataFrame(products)
    df2['來源'] = 'momo'
    df2['建立時間'] = datetime.today()
    # print(df2)

    return df2

def pchome(item):
    print('===== pchome =====')
    # 擷取網站
    url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={item}&page=1&sort=rnk/dc'
    re = requests.get(url).text
    d = json.loads(re)
    # print(d)

    # 整理資料
    products = []
    for i in d['prods']:
        product = {}
        product['網址'] = 'https://24h.pchome.com.tw/prod/' + i['Id']
        product['商品名稱'] = i['name']
        product['價格'] = i['price']
        product['圖片'] = 'https://b.ecimg.tw' + i['picS']
        products.append(product)
    # print(products, len(products))

    # 建立資料表
    df3 = pd.DataFrame(products)
    df3['來源'] = 'Pchome'
    df3['建立時間'] = datetime.today()
    # print(df3)

    return df3
