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

    return filtering_url, mg_url

@app.post("/items/list")
async def prodcut_list(item: listUrl):
    json = {}
    json["filtering"] = ProductList(item.filteringUrl)
    #json["magazines"] = MgProducts(item.magazineUrl)
    return json


@app.post("/items/details")
async def details_prompt(item: Url):
    simple_detail = SimpleDetail(item.productUrl)
    return simple_detail