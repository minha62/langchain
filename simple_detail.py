import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

from product_detail import ProductDetails

def SimpleDetail(url):
    details = ProductDetails(url)
    delivery = details["details"]["delivery"]
    size = str(details["size"]["size_info"])
    #review = str(details["up_reviews"][0])
    review = str(details["worst_reviews"][0])
    input = delivery + size + review

    os.environ['OPENAI_API_KEY']
    #os.environ.get('OPENAI_API_KEY')

    llm = OpenAI(temperature=0.9)

    template = """You are the helpful agent that summarizes product information from input contetns.
    - You should show size options. Don't add specific length(cm) for size.
    - You should let customers know the date of delivery arrival
    - You should show the summary of the review

    The result should be like below:
    Example1) 
    사이즈 옵션: S, M, L
    배송 정보: 10/7(토) 도착 예정
    가장 유용한 리뷰: 164cm, 49kg 여성은 M 사이즈를 구매했으며, "적당한 오버핏으로 길이도 제 키에 딱 맞아서 편하고 예뻐요! 후드티 핏이 아주 굿입니다." 라고 리뷰를 남겼습니다.

    Example2)
    사이즈 옵션: M, L
    배송 정보: 10/6(금) 도착 예정
    가장 유용한 리뷰: 162cm, 53kg 여성은 L 사이즈를 구매했으며, "품과 길이가 모두 만족스럽다"고 리뷰를 남겼습니다.

    Relevant information: {history}

    input contents: {input}
    result:"""


    prompt = PromptTemplate(
        input_variables=["history", "input"], 
        template=template
    )

    memory = ConversationKGMemory(llm=llm)
    history = []

    conversation_with_kg = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory
    )

    return conversation_with_kg.predict(input=input)