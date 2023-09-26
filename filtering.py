# https://python.langchain.com/en/latest/modules/memory/types/kg.html

# Bring in deps
import os
#from apikey import apikey

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

def Filtering(apikey, user_input):
    os.environ['OPENAI_API_KEY'] = apikey
    llm = OpenAI(temperature=0.5)

    template = """You are the helpful shopping agent that creates the filter that matches the user's input. You define the filters and choices in Typescript, and present the selected filters and choices as results using the given filter data.
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
        "name": "상의 중분류",
        "choices": (
          "001002": "셔츠/블라우스",
          "001006": "니트/스웨터",
          "001010": "긴팔 티셔츠",
          "001005": "맨투맨/스웨트셔츠",
          "001001": "반팔 티셔츠",
          "001003": "피케/카라 티셔츠",
          "001008": "기타 상의",
          "001004": "후드 티셔츠",
          "001011": "민소매 티셔츠"
        )
      ),
      (
        "name": "색상",
        "choices": (
            "2": "블랙",
            "1": "화이트",
            "36": "네이비",
            "23": "아이보리",
            "7": "블루",
            "24": "라이트 그레이",
            "5": "베이지",
            "37": "스카이 블루",
            "6": "그린",
            "25": "다크 그레이",
            "15": "기타 색상",
            "10": "핑크",
            "4": "브라운",
            "9": "옐로우",
            "32": "민트",
            "30": "카키",
            "11": "레드",
            "45": "라이트 핑크",
            "12": "오렌지",
            "8": "퍼플",
            "39": "라벤더",
            "29": "샌드",
            "44": "라이트 옐로우",
            "35": "다크 그린",
            "31": "라이트 그린",
            "34": "올리브 그린",
            "48": "페일 핑크",
            "49": "버건디",
            "16": "데님",
            "26": "카멜",
            "51": "딥레드",
            "28": "카키 베이지",
            "57": "연청",
            "13": "실버",
            "58": "중청",
            "60": "흑청",
            "59": "진청",
            "14": "골드",
            "56": "로즈골드"
        )
      )
      (
        "name": "정렬",
        "choices": (
          "": "무신사 추천순",
          "new": "신상품(재입고)순",
          "price_row": "낮은 가격순",
          "price_high": "높은 가격순",
          "discount_rate": "할인율순",
          "emt_high": "후기순"
          "sale_high": "판매순"
        )
      )
    ]```

    If there is something not including in Filter, you have to add "&includeKeywords=" and the component like this.
    user input:2만원대 하늘색 로고 반팔 티셔츠 찾아줘
    URL:https://www.musinsa.com/categories/item/001001?color=37&price1=20000&price2=29999&includeKeywords=로고

    
    If there is something related to period when using filtering "정렬", add "&sub_sort=" and the component like this.
      Ex1) 1일 = &sub_sort=1d
      Ex2) 1주일 = &sub_sort=1w
      Ex3) 3개월 = &sub_sort=3m
      Ex4) 2년 = &sub_sort=2y

    Example 1)
    user input:40,000원 이하 스트라이프 블랙 니트를 찾아줘
    URL:https://www.musinsa.com/categories/item/001006?color=2&price1=0&price2=40000&includeKeywords=스트라이프

    Example 2)
    user input:3만원대 린넨 셔츠를 찾아줘
    URL:https://www.musinsa.com/categories/item/001002?price1=30000&price2=39999&includeKeywords=린넨

    Example 3)
    user input:4만원대 브라운 맨투맨 추천해줘. 4개월 동안 판매가 많은순으로 정렬해줘.
    URL:https://www.musinsa.com/categories/item/001005?color=4&price1=40000&price2=49999&sort=sale_high&sub_sort=4m
    
    Relavant Information: 
    {history}

    Conversation:
    user input:{input}
    URL:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"], 
        template=template
    )

    memory = ConversationKGMemory(llm=llm)
    memory.save_context({"input":"..."}, {"output":"..."})
    memory.save_context({"input":"..."}, {"output":"..."})

    conversation_with_kg = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )

    return conversation_with_kg.predict(input=user_input).replace('"', '')