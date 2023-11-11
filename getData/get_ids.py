from bs4 import BeautifulSoup
import requests
from crawling.category import categoryList

def GetIDs(root_url):
    response = requests.get(root_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    searchList = soup.find('ul', id='searchList')
    list = searchList.find_all('li', class_='li_box')
    # print(len(list)) # 90개

    ids = []
    for i in range(len(list)):
        cl = list[i]
        id = cl.get('data-no')
        ids.append(id)
    return ids


def GetCategoryIDs():
    category_ids=[]
    for category in categoryList:
        for key, _ in category.items():
            url = 'https://www.musinsa.com/categories/item/' + key
            # category_ids.append({key:GetIDs(url)})
            category_ids.append((key, GetIDs(url)))
    return category_ids


# print(GetCategoryIDs())