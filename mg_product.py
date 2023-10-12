from bs4 import BeautifulSoup
import requests

def MgProducts(mg_search_url):
    #step1 : Download the webpage
    response = requests.get(mg_search_url)
    html_content = response.text

    #step2 : Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    mg_list = soup.find_all('li', class_='listItem')
    mg_urls = []
    # Limit the loop to the first 5 items
    for unit in mg_list[:10]:
        # Get product URL
        mg_url = unit.find('div', class_='articleInfo').a.get('href')
        if "magazine" in mg_url or "news" in mg_url:
            mg_urls.append(mg_url)
    print(len(mg_urls))

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

        if goods_units:
            for unit in goods_units[:5]: # 한 매거진마다 5개 상품 가져오기
                # 상품 9개 가져오면 종료
                if len(mg_clothes) >= 9: break

                unit = goods_units[i]

                # Get goods number
                goods_no = unit.get('goods_no')

                # Get product brand
                product_brand = unit.find('a', class_='brand').get_text()

                info = unit.find('a', class_='name')

                # Get product name
                product_name = info.get_text()

                # Get product URL
                product_url = info.get('href')

                img_url = unit.find('img').get('data-src')
                if "https:" not in img_url:
                    img_url = "https:" + img_url
                if requests.get(img_url).status_code != 200:
                    # print("error", img_url)
                    continue

                price = unit.find('span', class_='price').get_text()

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
    print(len(mg_clothes))

    return {"result": result, "clothes": mg_clothes}


url = "https://www.musinsa.com/search/musinsa/magazine?q=y2k"
print(MgProducts(url))
# MgProducts(url)