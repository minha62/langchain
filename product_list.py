from bs4 import BeautifulSoup
import requests

def ProductList(filtering_url):
    url = filtering_url
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    searchList = soup.find('ul', id='searchList')
    list = searchList.find_all('li', class_='li_box')

    clothes = []
    for i in range(5):
        cl = list[i]
        num = cl.get('data-no')

        element = cl.find('div', class_='li_inner')

        url = element.find('a', class_='img-block').get('href')
        img = element.find('img', class_='lazyload lazy').get('data-original')
        #brand = element.find('p', class_='item_title').find('a').text
        title = element.find('p', class_='list_info').find('a').text.strip() if element.find('p', class_='list_info') else None

        price = element.find('p', class_='price') if element.find('p', class_='price') else None
        orig_price = price.find('del').text.strip() if element.find('del') else None
        discounted_price = price.get_text(strip=True).replace(orig_price, '') if orig_price else price.text.strip()

        info = {
            "no": num,
            "img": img,
            "title": title,
            "price": discounted_price,
            "url": url,
        }
        clothes.append(info)

    return clothes