#from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, constr
from filtering import Filtering

class Item(BaseModel):
    prompt: constr(min_length=1)

app = FastAPI()

@app.post("/lang/")
async def filtering_prompt(item: Item):
    url = Filtering(item)
    return url