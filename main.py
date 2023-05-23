from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel
from filtering import Filtering

class Item(BaseModel):
    prompt: Any

app = FastAPI()

@app.post("/lang/")
async def filtering_prompt(item: Item):
    url = Filtering(item)
    return url