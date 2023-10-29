#from typing import Any
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
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    apikey: str
    userNeed: str

class listUrl(BaseModel):
    filteringUrl: str
    magazineUrl: str

class Url(BaseModel):
    productUrl: str

class Detail(BaseModel):
    apikey: str
    productUrl: str

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


# @app.post("/items/")
# async def search(item: Item):
#     filtering_url = Filtering(item.apikey, item.userNeed)
#     print(filtering_url)
#     json = {}
#     json["filtering"] = ProductList(filtering_url)

#     mg_url = Magazine(item.apikey, item.userNeed)
#     print(mg_url)
#     json["magazines"] = MgProducts(mg_url)
#     return json

@app.post("/items/filtering")
async def search(item: Item):
    filtering_url = Filtering(item.apikey, item.userNeed)
    print(filtering_url)
    json = {}
    json["filtering"] = ProductList(filtering_url)
    return json

@app.post("/items/magazines")
async def search(item: Item):
    mg_url = Magazine(item.apikey, item.userNeed)
    print(mg_url)
    json = {}
    json["magazines"] = MgProducts(mg_url)
    return json

@app.post("/items/details")
async def simple_detail(item: Detail):
    # details = Details(item.apikey, item.productUrl) # simple_detail + size_reco + review_summ 한번에 => timeout error
    return SimpleDetail(item.apikey, item.productUrl)

@app.post("/items/details/size")
async def size_reco(item: Detail):
    return SizeReco(item.apikey, item.productUrl)

@app.post("/items/details/review")
async def review_summ(item: Detail):
    return ReviewSumm(item.apikey, item.productUrl)