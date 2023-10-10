import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

from get_simple_detail import GetSimpleDetail

def gpt(input, template):
    llm = OpenAI(temperature=0.9)

    prompt = PromptTemplate(
        input_variables=["history", "input"], 
        template=template
    )

    memory = ConversationKGMemory(llm=llm)

    conversation_with_kg = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )

    return conversation_with_kg.predict(input=input).strip()

def SimpleDetail(apikey, url):
    os.environ['OPENAI_API_KEY'] = apikey
    simple_detail = GetSimpleDetail(url)
    delivery = simple_detail["delivery"]
    size_info = str(simple_detail["size_info"])
    best_review = str(simple_detail["best_review"])
    
    input = delivery + size_info + best_review

    simple_detail_template = """You are the helpful agent that summarizes product information from input contents. You should show size options. Don't add specific length(cm) for size. You should let customers know the date of delivery arrival. You should show the summary of the review if review is not None. You have to finish the reveiw summary sentence.
    The result should be like this: Example1)사이즈 옵션은 총 3가지로 S, M, L이 있습니다. 상품은 10/7(토) 도착 예정입니다. 가장 유용한 리뷰: 여성 · 164cm · 49kg 고객이 M 사이즈를 구매했으며, "적당한 오버핏으로 길이도 키에 딱 맞아서 편하고 예쁘고 후드티 핏이 좋다"고 리뷰를 남겼습니다. Example2)사이즈 옵션은 총 2가지로 M, L이 있습니다. 상품은 10/6(금) 도착 예정입니다. 가장 유용한 리뷰: 여성 · 162cm · 53kg 고객이 L 사이즈를 구매했으며, "품과 길이가 모두 만족스럽다"고 리뷰를 남겼습니다.
    If profile in the review is None, the result should be like this: Example)사이즈 옵션은 총 1가지로 FREE이 있습니다. 상품은 10/12(목) 도착 예정입니다. 가장 유용한 리뷰: 비회원 고객이 FREE 사이즈를 구매했으며, "색상은 상세페이지와 비슷하지만 사이즈가 매우 크다" 리뷰를 남겼습니다.
    If review is None, the result should be like this: Example)사이즈 옵션은 총 1가지로 ONE이 있습니다. 상품은 10/10(화) 도착 예정입니다. 아직 리뷰가 없습니다.
    Relevant information:{history} input contents:{input} result:"""

    simple_detail = gpt(input, simple_detail_template)

    return { 
        "simple_detail": simple_detail,
        }

# from apikey import apikey
# url = 'https://www.musinsa.com/app/goods/3056893'
# print(Details(apikey, url))