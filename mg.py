from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from bs4 import BeautifulSoup
import requests


#각 매거진에서 관련상품 정보 얻어오는 함수
def GetItems(mg_urls):
    mg_clothes = []
    result = True

    #상품 개수가 30개가 될때까지 반복
    while len(mg_clothes) < 30:
        for i in range(len(mg_urls)):
            # Chrome 옵션 설정
            options = webdriver.ChromeOptions()
            #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") # for heroku
            options.add_argument('--headless')  # 브라우저 창 숨기기
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')

            #service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # local
            #driver = webdriver.Chrome(service=service, options=options) # for heroku
            url = mg_urls[i]
            driver.get(url)
            
            page_html = driver.page_source

            soup = BeautifulSoup(page_html, 'html.parser')

            #관련상품
            goods_units = soup.find_all('li', class_='goods-unit')

            if goods_units:  # Check if the list is not empty
                for unit in goods_units[:min(10, len(goods_units))]:
        

                    # Get goods number
                    goods_no = unit.get('goods_no')

                    # Get image URL
                    img_element = unit.find('img', class_='lazy-img')
                    if img_element:
                        img_url = img_element.get('data-src')
                    else:
                        img_url = None

                    # Get product URL
                    div_element = unit.find('div', class_='img')
                    if div_element and div_element.a:
                        product_url = div_element.a.get('href')
                    else:
                        product_url = None

                    # Get product name
                    name_element = unit.find('a', class_='name')
                    if name_element:
                        product_name = name_element.text
                    else:
                        product_name = None

                    # Get product price
                    price_element = unit.find('span', class_='price')
                    if price_element:
                        price = price_element.text
                    else:
                        price = None

                    info = {
                        "no": goods_no,
                        "img": img_url,
                        "title": product_name,
                        "price" : price,
                        "url" : product_url,
                    }

                    # 모든 값들이 None이 아닌 경우에만 append
                    if all([info[key] for key in info]):
                        mg_clothes.append(info)

                    # mg_clothes의 데이터가 30개 이상이면 루프 종료
                    if len(mg_clothes) >= 30:
                        break
        # mg_urls의 모든 URL을 순회한 후에도 mg_clothes의 데이터가 30개 미만이면 루프 종료
        else:
            break

    if len(mg_clothes) == 0:
        result = False
    else:
        result = True
    return {"result": result, "clothes": mg_clothes}

def MgProducts(mg_url):
    #step1 : Download the webpage
    response = requests.get(mg_url)
    html_content = response.text

    #step2 : Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    mg_list = soup.find_all('li', class_='listItem')
    mg_urls = []

    #상위 50개 매거진 url 얻어오기
    for index, unit in enumerate(mg_list[:50]):
        # Get product URL
        mg_url = unit.find('div', class_='articleImg').a.get('href')
        mg_urls.append(mg_url)
        #print(f"Product URL: {mg_url}")
        #print("-" * 50)
    GetItems(mg_urls)

#mg_url = "https://www.musinsa.com/search/musinsa/magazine?q=y2k"
#print(MgProducts(mg_url))