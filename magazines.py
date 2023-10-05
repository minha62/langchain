import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

from bs4 import BeautifulSoup
import requests

def Magazine(user_input):
    # def get_imgUrl(url):
    #     response = requests.get(url)
    #     html_content = response.text

    #     soup = BeautifulSoup(html_content, 'html.parser')

    #     print(soup)
    #     element = soup.find('meta', attrs={'property': 'og:image'})
    #     print(element)
    #     img_url = element['content']
    #     return img_url

    os.environ['OPENAI_API_KEY']
    llm = OpenAI(temperature=0.9)

    template = """You are the helpful agent that creates url that matches the user's input.
    - output should be only one URL. do not add any description about output.

    If there is something related to shopping keywords, you have to add "?q=" and the component like this.
    You don't have to care about categories of clothes like bags, tops, skirts, jeans and so on.

    Do not add another filter or component like sorting, price and so on.

    Example 1)
    user input: 키치한 옷 찾아줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=키치

    Example 2)
    user input: 연예인이 착용한 가방 보여줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=연예인착용

    Example 3)
    user input: 힙한 옷 보여줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=힙한

    Example 4)
    user input: y2k 패션 추천해줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=y2k

    Relavant Information:
    {history}

    Conversation:
    user input: {input}
    URL:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )

    memory = ConversationKGMemory(llm=llm)
    memory.save_context({"input":"요즘 인기있는 스타일 보여줘"}, {"output":"https://www.musinsa.com/search/musinsa/magazine?q=인기있는"})

    conversation_with_kg = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )

    mg_search_url = conversation_with_kg.predict(input=user_input)

    #step1 : Download the webpage
    url= mg_search_url
    print(url)
    response = requests.get(url)
    html_content = response.text

    #step2 : Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    mg_list = soup.find_all('li', class_='listItem')
    mg_urls = []
    # Limit the loop to the first 5 items
    for unit in mg_list[5:10]:
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

        if goods_units:  # Check if the list is not empty
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

            # Get image URL
            img_url = unit.find('img').get('data-src')
            # img_url = get_imgUrl(product_url)

            # Get product price
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

    return {"result": result, "clothes": mg_clothes}