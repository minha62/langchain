from bs4 import BeautifulSoup
import requests

def ProductList(filtering_url):
    result = True
    url = filtering_url
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    searchList = soup.find('ul', id='searchList')
    list = searchList.find_all('li', class_='li_box')
    # print(len(list)) # 90개

    clothes = []
    for i in range(len(list)):
        if len(clothes) > 27: break
        cl = list[i]
        num = cl.get('data-no')

        element = cl.find('div', class_='li_inner')

        if element.find('a', class_='img-block').get('href'):
            url = element.find('a', class_='img-block').get('href')
        else: continue

        if element.find('img', class_='lazyload lazy').get('data-original'):
            img = element.find('img', class_='lazyload lazy').get('data-original')
        else: continue

        if element.find('p', class_='item_title').find('a'):
            brand = element.find('p', class_='item_title').find('a').text
        else: continue

        if element.find('p', class_='list_info'):
            title = element.find('p', class_='list_info').find('a').text.strip()
        else: continue

        if element.find('p', class_='price'):
            price = element.find('p', class_='price') 
        else: continue

        if element.find('del'):
            orig_price = price.find('del').text.strip() 
        else: continue

        discounted_price = price.get_text(strip=True).replace(orig_price, '') if orig_price else price.text.strip()

        info = {
            "no": num,
            "name": title,
            "brand": brand,
            "price": discounted_price,
            "img": img,
            "url": 'https:' + url,
        }
        clothes.append(info)
    if len(clothes) == 0:
        result = False
    return {"result": result, "clothes": clothes}