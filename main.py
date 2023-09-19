#from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from filtering import Filtering
from details import Details
from typing import Callable, Dict

class Item(BaseModel):
    apikey: str
    prompt: str

class Detail(BaseModel):
    brand: str
    name: str
    score: float
    oirg_price: str
    discount_price: str
    cust_summary: Callable[[str, str], str]
    size: Dict[str, float]
    delivery: str
    

app = FastAPI()

@app.post("/items/")
async def filtering_prompt(item: Item):
    url = Filtering(item.apikey, item.prompt)
    return url

@app.post("/lang/details")
async def details_prompt():
    detail = Details()
    return detail