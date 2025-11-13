# from fastapi_exp import sqlmodel_example
# from fastapi import sql_model
from typing import Union, Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
# from previous work in other files
from datetime import date, datetime
from decimal import Decimal
# import json  # FastAPI may accommodate all JSON formatting :)
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional


'''
# Included for basic FastAPI checks
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool] = None
'''


# This is used by read_employees()
class Employees(SQLModel, table=True):
    employee_id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=25, nullable=False)
    email: str = Field(max_length=100, nullable=False)
    phone_number: str = Field(max_length=20)
    hire_date: date = Field(nullable=False)
    job_id: int = Field(nullable=False)
    salary: Decimal = Field(nullable=False)
    manager_id: Optional[int] = Field(default=None)
    department_id: int = Field(default=None)


# This may not be needed because FastAPI may take care of this automatically
def serialize_json(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)  # originally str, float works although not necessarily to two decimal places
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


# Our database url
DATABASE_URL = "postgresql://<user>:<password>>@<server>:<tcp-port>/<database>"

engine = create_engine(DATABASE_URL, echo=True)  # format from previous file


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.get("/data/export/hr_sample/tables/employees/")
def read_employees(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Employees]:
    # statement = select(Employees)
    employees = session.exec(select(Employees))
    return employees


'''
# Basic functionality checks
@app.get("/")
def read_root():
    return {'message': 'Hello World'}


# Basic functionality checks
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Basic functionality checks
@app.put("/items/{item_id}")
def update_item(item_id: int, item_name: str):
    return {"item_name": item_name, "item_id": item_id}


@app.get('/data/export/hr_sample/all')
def export_hr_sample_data():
    return {'message': 'Placeholder for a hr_sample database export.'}


@app.get('/data/export/hr_sample/tables/employee/all_rows')
def export_hr_sample_data(table: str, action: str):
    # return {'message': 'Placeholder for returning the hr_sample employees table.'}
    return{"employee_id": employee_id, "first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "hire_date": hire_date, "job_id": job_id, "salary": salary, "manager_id": manager_id, "department_id": department_id}


@app.get('/data/export/hr_sample/tables/employee/changes')
def export_all_hr_sample_data():  # from_date: datetime, to_date: datetime
    return {'message': 'Placeholder for hr_sample database export using time-based query parameters.  If a to_date is '
                       'not included, the current date defaults to current date 0000 UTC.'}
'''
