from datetime import datetime
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool] = None


@app.get("/")
def read_root():
    return {'message': 'Hello World'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item_name, "item_id": item_id}


@app.get('/data/export/hr_sample/all')
def export_all_hr_sample_data():
    return {'message': 'Placeholder for hr_sample database export.'}


@app.get('/data/export/hr_sample/all/changes')
def export_all_hr_sample_data():  # from_date: datetime, to_date: datetime
    return {'message': 'Placeholder for hr_sample database export using time-based query parameters.  If a to_date is '
                       'not included, the current date defaults to current date 0000 UTC.'} 
