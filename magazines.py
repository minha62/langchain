import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

from bs4 import BeautifulSoup
import requests

def Magazine(apikey, user_input):
    os.environ['OPENAI_API_KEY'] = apikey
    llm = OpenAI(temperature=0.9)

    template = """You are the helpful agent that creates the filter that matches the user's input. You define the filters and choices in Typescript, and present the selected filters and choices as results using the given filter data.
    - An OR operation is performed between the choices.
    - output should be only one URL. do not add any description about output.
    - The filter name and choices given to the data in typescript file should be written exactly as it is.

    ```TypeScript
    interface Filter (
      name: string;
      choices: ( [code: string]: string );
    );

    //data
    const filters: Filter[] = [
      (
        "name": "정렬",
        "choices": (
          "create_date": "최신순",
          "hit": "조회순",
          "total_comment_count": "많은댓글순",
          "comment_date": "최신댓글순"
        )
      )
    ]```

    If there is something not including in Filter, you have to add "includeKeywords=" and the component like this.


    Example 1)
    user input: 키치한 옷 찾아줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=키치&sortCode=create_date

    Example 2)
    user input: 연예인이 착용한 가방 보여줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=연예인착용&sortCode=create_date

    Example 3)
    user input: 힙한 옷 보여줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=힙한&sortCode=create_date

    Example 4)
    user input: y2k 패션 추천해줘
    URL: https://www.musinsa.com/search/musinsa/magazine?q=y2k&sortCode=create_date

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
    memory.save_context({"input":"요즘 인기있는 스타일 보여줘"}, {"output":"https://www.musinsa.com/search/musinsa/magazine?q=인기있는&sortCode=create_date"})
    memory.save_context({"input":"연예인이 착용한 옷들 보여줘"}, {"output":"https://www.musinsa.com/search/musinsa/magazine?q=연예인착용&sortCode=create_date"})

    conversation_with_kg = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )

    mg_search_url = conversation_with_kg.predict(input=user_input)

    #step1 : Download the webpage
    url= mg_search_url
    response = requests.get(url)
    html_content = response.text

    #print(response)
    #print(html_content)

    #step2 : Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    mg_list = soup.find_all('li', class_='listItem')
    mg_urls = []
    # Limit the loop to the first 5 items
    for index, unit in enumerate(mg_list[:5]):

        # Get product URL
        mg_url = unit.find('div', class_='articleImg').a.get('href')
        mg_urls.append(mg_url)
        #print(f"Product URL: {mg_url}")
        #print("-" * 50)

    mg_clothes = []
    #step1 : Download the webpage
    for i in range(len(mg_urls)):
      url = mg_urls[i]
      response = requests.get(url)
      html_content = response.text

      #print(response)
      #print(html_content)

      #step2 : Parse the HTML
      soup = BeautifulSoup(html_content, 'html.parser')

      #step3 : 관련상품 url 가져오기
      goods_units = soup.find_all('li', class_='goods-unit')

      if goods_units:  # Check if the list is not empty
        unit = goods_units[0]  # Get the first product

        # Get goods number
        goods_no = unit.get('goods_no')

        # Get image URL
        img_url = unit.find('img', class_='lazy-img').get('data-src')

        # Get product URL
        product_url = unit.find('div', class_='img').a.get('href')

        # Get product name
        product_name = unit.find('a', class_='name').text

        # Get product price
        price = unit.find('span', class_='price').text

        info = {
            "no": goods_no,
            "img": img_url,
            "title": product_name,
            "price" : price,
            "url" : product_url,
        }
        mg_clothes.append(info)
        
    return mg_clothes