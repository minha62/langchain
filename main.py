#from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from filtering import Filtering
from product_list import ProductList
from simple_detail import SimpleDetail
from magazines import Magazine

class Item(BaseModel):
    userNeed: str

class Url(BaseModel):
    productUrl: str

app = FastAPI()

@app.post("/items/")
async def filtering_prompt(item: Item):
    url = Filtering(item.userNeed)
    print(url)

    json = {}
    json["filtering"] = ProductList(url)
    json["magazines"] = Magazine(item.userNeed)
    return json

@app.post("/items/details")
async def details_prompt(item: Url):
    simple_detail = await SimpleDetail(item.productUrl)
    return simple_detail