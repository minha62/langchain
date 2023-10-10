from bs4 import BeautifulSoup
import requests
import re
from urllib.request import Request, urlopen

def MgProducts(mg_search_url):
    #step1 : Download the webpage
    url= mg_search_url
    response = requests.get(url)
    html_content = response.text

    #step2 : Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    mg_list = soup.find_all('li', class_='listItem')
    mg_urls = []
    # Limit the loop to the first 15 items
    for unit in mg_list[:15]:
        # Get product URL
        mg_url = unit.find('div', class_='articleInfo').a.get('href')
        mg_urls.append(mg_url)

    result = True
    mg_clothes = []
    #step1 : Download the webpage
    for i in range(len(mg_urls)):
        url = mg_urls[i]
        response = requests.get(url)
        html_content = response.text

        #step2 : Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        #step3 : 관련상품 url 가져오기
        goods_units = soup.find_all('li', class_='goods-unit')

        if goods_units and len(mg_clothes) < 6:  # Check if the list is not empty
            unit = goods_units[0]  # Get the first product

            # Get goods number
            goods_no = unit.get('goods_no')

            # Get product brand
            product_brand = unit.find('a', class_='brand').get_text()

            info = unit.find('a', class_='name')

            # Get product name
            product_name = info.get_text()

            # Get product URL
            product_url = info.get('href')

            # Move to product url
            url = Request(product_url, headers={'User-Agent':'Mozilla/5.0'})
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Get image URL
            meta_tag_img = soup.find('meta', property='og:image')
            if meta_tag_img:
                img_url = meta_tag_img.get('content')
            else:
                continue
            # img_url = unit.find('img').get('data-src')
            # img_url = get_imgUrl(product_url)

            # Get product price
            meta_tag_price = soup.find('meta', property='og:description')
            if meta_tag_img:
                description = meta_tag_price['content']
                price = re.search(r'(\d{1,3}(?:,\d{3})+)', description).group(1)+'원'
            else:
                continue
            # price = unit.find('span', class_='price').get_text()

            info = {
                "no": goods_no,
                "name": product_name,
                "brand": product_brand,
                "price" : price,
                "img": img_url,
                "url" : product_url,
            }
            mg_clothes.append(info)

    if len(mg_clothes)==0:
        result = False

    return {"result": result, "clothes": mg_clothes}