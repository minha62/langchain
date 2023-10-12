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

@app.post("/items/")
async def search(item: Item):
    filtering_url = Filtering(item.apikey, item.userNeed)
    print(filtering_url)
    json = {}
    json["filtering"] = ProductList(filtering_url)

    mg_url = Magazine(item.apikey, item.userNeed)
    print(mg_url)
    json["magazines"] = MgProducts(mg_url)
    return json

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