#from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from filtering import Filtering
from product_list import ProductList
from product_details import Details
from magazines import Magazine
from mg_product import MgProducts

class Item(BaseModel):
    apikey: str
    userNeed: str

class listUrl(BaseModel):
    filteringUrl: str
    magazineUrl: str

class Url(BaseModel):
    productUrl: str

app = FastAPI()

# 상태 변수를 추가하고 초기값을 설정
app.state.apikey = None

@app.post("/items/")
async def search(item: Item):
    app.state.apikey = item.apikey

    filtering_url = Filtering(item.apikey, item.userNeed)
    print(filtering_url)

    mg_url = Magazine(item.apikey, item.userNeed)
    print(mg_url)
    return {"filteringUrl": filtering_url, "magazineUrl": mg_url}

@app.post("/items/ftList")
async def prodcut_list(item: Url):
    json = {}
    json["filtering"] = ProductList(item.productUrl)
    #json["magazines"] = MgProducts(item.magazineUrl)
    return json

@app.post("/items/mgList")
async def magazine_list(item: Url):
    json = {}
    #json["filtering"] = ProductList(item.filteringUrl)
    json["magazines"] = MgProducts(item.productUrl)
    return json


@app.post("/items/details")
async def product_details(item: Url):
    apikey = app.state.apikey
    details = Details(apikey, item.productUrl)
    return details