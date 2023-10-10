import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

from product_element import ProductElements
from product_detail_test import ProductDetails

def gpt(apikey, input, template):
    os.environ['OPENAI_API_KEY'] = apikey

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

def Details(apikey, url):
    details = ProductDetails(url)
    delivery = details["details"]["delivery"]
    size_info = str(details["size"]["size_info"])
    size_reco = str(details["size"]["size_reco"])
    up_reviews = details["up_reviews"]
    worst_reviews = details["worst_reviews"]
    if up_reviews:
        best_review = str(up_reviews[0])
    else:
        best_review = None
    
    input = delivery + size_info + best_review

    simple_detail_template = """You are the helpful agent that summarizes product information from input contents. You should show size options. Don't add specific length(cm) for size. You should let customers know the date of delivery arrival. You should show the summary of the review if review is not None. You have to finish the reveiw summary sentence.
    The result should be like this: Example1)사이즈 옵션은 총 3가지로 S, M, L이 있습니다. 상품은 10/7(토) 도착 예정입니다. 가장 유용한 리뷰: 여성 · 164cm · 49kg 고객이 M 사이즈를 구매했으며, "적당한 오버핏으로 길이도 키에 딱 맞아서 편하고 예쁘고 후드티 핏이 좋다"고 리뷰를 남겼습니다. Example2)사이즈 옵션은 총 2가지로 M, L이 있습니다. 상품은 10/6(금) 도착 예정입니다. 가장 유용한 리뷰: 여성 · 162cm · 53kg 고객이 L 사이즈를 구매했으며, "품과 길이가 모두 만족스럽다"고 리뷰를 남겼습니다.
    If profile in the review is None, the result should be like this: Example)사이즈 옵션은 총 1가지로 FREE이 있습니다. 상품은 10/12(목) 도착 예정입니다. 가장 유용한 리뷰: 비회원 고객이 FREE 사이즈를 구매했으며, "색상은 상세페이지와 비슷하지만 사이즈가 매우 크다" 리뷰를 남겼습니다.
    If review is None, the result should be like this: Example)사이즈 옵션은 총 1가지로 ONE이 있습니다. 상품은 10/10(화) 도착 예정입니다. 아직 리뷰가 없습니다.
    Relevant information:{history} input contents:{input} result:"""

    simple_detail = gpt(apikey, input, simple_detail_template)

    if size_reco:
        size_reco_template = """You are the helpful agent that recommends height and weight per size options from input size contents. Calculate average range of heights and weights per sizes and sex. If there is no data in one size option, don't print height and weight but "데이터 없음".
    The result should be like this: Example1)[S size] (여성)155~160cm/45~50kg, (남성)데이터 없음\n[M size] (여성)160~165cm/50~60kg, (남성)170~175cm/64~77kg\n[L size] (여성)165~170cm/60~70kg, (남성)175~180cm/77~100kg Example2)[FREE size] (여성)160~168cm/48~63kg, (남성)172~185cm/62~84kg
    Relevant information:{history} size contents:{input} result:"""
        sizeReco = "구매자 통계를 기반으로 사이즈를 추천드리겠습니다.\n" + gpt(apikey, str(size_reco), size_reco_template)
    else:
        sizeReco = "아직 구매자가 없어 추천이 어렵습니다." # 추후 사이즈표 제시

    if up_reviews:
        review_sum_template = """You are the helpful agent that summarize reviews. The output has to be 2~3 sentences in Korean. Relevant information:{history} review contents:{input} result:"""
        #  The result should be like this: Example)제품의 품이 넉넉하고 디자인은 이쁘지만 물때가 있어서 검수가 필요해 보인다는 의견이 있었습니다. 핏이 널널하고 예쁘다고 말하는 고객도 있지만, 핏이 아방해서 마음에 들지 않는다는 고객도 있습니다. Example2)시보리가 짱짱해서 마음에 들고, 블랙과 핑크 조합이 귀엽고, 예쁜 디자인과 색상으로 인기가 많다는 평이 있습니다. 품질과 핏이 좋지만 목부분이 살짝 감긴다는 의견이 있습니다.
        up_sum = gpt(apikey, str(up_reviews[1:]), review_sum_template)
        worst_sum = gpt(apikey, str(worst_reviews), review_sum_template)
        reviewSum = "구매자들의 리뷰를 유용한 리뷰와 평점이 낮은 리뷰로 나눠서 요약해드리겠습니다.\n" + "[유용한 리뷰] " + up_sum + "\n[낮은 평점 리뷰] " + worst_sum
    else:
        reviewSum = "리뷰가 존재하지 않습니다."

    return {
            "details": {
                "simple_detail": simple_detail,
                "size_reco": sizeReco,
                "review_sum": reviewSum
            }
        }

from apikey import apikey
url = 'https://www.musinsa.com/app/goods/3056893'
print(Details(apikey, url))