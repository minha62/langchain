import os

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

from get_reviews import GetReviews

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

def ReviewSumm(apikey, url):
    os.environ['OPENAI_API_KEY'] = apikey
    up_reviews, worst_reviews = GetReviews(url)
    input = str({"best_reviews": up_reviews, "worst_reviews": worst_reviews})

    if up_reviews:
        review_sum_template = """You are the helpful agent that summarize best reviews and worst reviews as 2~3 sentences separately.
        The result should be like this: Example)[유용한 리뷰] 시보리가 짱짱해서 마음에 들고, 블랙과 핑크 조합이 귀엽고, 예쁜 디자인과 색상으로 인기가 많다는 평이 있습니다.\n[낮은 평점 리뷰] 품질과 핏이 좋지만 목부분이 살짝 감긴다는 의견이 있습니다.
        Relevant information:{history} reviews:{input} result:"""
        #up_summ = gpt(str(up_reviews[1]), review_sum_template)
        #worst_summ = gpt(str(worst_reviews[0]), review_sum_template)
        #reviewSumm = "구매자들의 리뷰를 유용한 리뷰와 평점이 낮은 리뷰로 나눠서 요약해드리겠습니다.\n" + "[유용한 리뷰] " + up_summ + "\n[낮은 평점 리뷰] " + worst_summ
        reviewSumm = "구매자들의 리뷰를 유용한 리뷰와 평점이 낮은 리뷰로 나눠서 요약해드리겠습니다.\n" + gpt(input, review_sum_template)
    else:
        reviewSumm = "리뷰가 존재하지 않습니다."

    return { 
            "review_summ": reviewSumm
        }