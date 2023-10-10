#from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from filtering import Filtering
from product_list import ProductList
from simple_detail import SimpleDetail
from magazines import Magazine
from mg_product import MgProducts

class Item(BaseModel):
    userNeed: str

class listUrl(BaseModel):
    filteringUrl: str
    magazineUrl: str

class Url(BaseModel):
    productUrl: str

app = FastAPI()

@app.post("/items/")
async def filtering_prompt(item: Item):
    filtering_url = Filtering(item.userNeed)
    print(filtering_url)

    mg_url = Magazine(item.userNeed)
    print(mg_url)

    json = {}
    json["filtering"] = ProductList(filtering_url)
    json["magazines"] = MgProducts(mg_url)
    return json
    #return filtering_url, mg_url

@app.post("/items/ftList")
async def prodcut_list(item: Url):
    json = {}
    json["filtering"] = ProductList(item.productUrl)
    #json["magazines"] = MgProducts(item.magazineUrl)
    return json

@app.post("/items/mgList")
async def prodcut_list(item: Url):
    json = {}
    #json["filtering"] = ProductList(item.filteringUrl)
    json["magazines"] = MgProducts(item.productUrl)
    return json


@app.post("/items/details")
async def details_prompt(item: Url):
    simple_detail = SimpleDetail(item.productUrl)
    return simple_detail