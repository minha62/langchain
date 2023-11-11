#from typing import Any
from cache_utils import cache
from fastapi import FastAPI
from pydantic import BaseModel
from filtering import Filtering
from product_list import ProductList
from magazines import Magazine
from mg_product import MgProducts
# from product_details_all import Details
from simple_detail import SimpleDetail
from size_reco import SizeReco
from review_summ import ReviewSumm
from ask import Ask
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    apikey: str
    userNeed: str

class Detail(BaseModel):
    apikey: str
    id: str

class Question(BaseModel):
    apikey: str
    user_question: str
    id: str

app = FastAPI()

# origins에는 protocal, domain, port만 등록
origins = [
    # "http://192.168.0.13:3000", # url을 등록해도 되고
    "*" # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부 설정. default는 False
    allow_methods=["*"],    # 허용할 method 설정. default는 GET
    allow_headers=["*"],	# 허용할 http header 목록 설정. Content-Type, Accept, Accept-Language, Content-Language은 항상 허용
)


@app.post("/items/filtering")
async def search(item: Item):
    filtering_url = Filtering(item.apikey, item.userNeed)

    # Use the url to generate a unique cache key
    cache_key = filtering_url

    # Check if the result is already in the cache
    result = cache.get(cache_key)

    if result is None:
        # If not, perform ProductList and store the result in the cache
        result = ProductList(filtering_url)
        cache[cache_key] = result
    return {"filtering":result}

@app.post("/items/magazines")
async def search(item: Item):
    mg_url = Magazine(item.apikey, item.userNeed)

     # Use the url to generate a unique cache key
    cache_key = mg_url

    # Check if the result is already in the cache
    result = cache.get(cache_key)

    if result is None:
        # If not, perform ProductList and store the result in the cache
        result = MgProducts(mg_url)
        cache[cache_key] = result
    return {"magazines":result}

@app.post("/items/details")
async def simple_detail(item: Detail):
    cache_key = f"{item.id}_simple_detail"
    result = cache.get(cache_key)
    if result is None:
        result = SimpleDetail(item.id)
        cache[cache_key] = result
    return result

@app.post("/items/details/size")
async def size_reco(item: Detail):
    cache_key = f"{item.id}_size_reco"
    result = cache.get(cache_key)
    if result is None:
        result = SizeReco(item.apikey, item.id)
        cache[cache_key] = result
    return result

@app.post("/items/details/review")
async def review_summ(item: Detail):
    cache_key = f"{item.id}_review_summ"
    result = cache.get(cache_key)
    if result is None:
        result = ReviewSumm(item.apikey, item.id)
        cache[cache_key] = result
    return result

@app.post("/items/ask")
async def question_ask(item: Question):
    return Ask(item.apikey, item.user_question, item.id)