from db import db

from typing import List, Optional
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from bson import ObjectId


app = FastAPI()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class StuffModel(BaseModel):
    '''Generic Model Item'''
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field()
    description: Optional[str] = None
    categories: List[str] = []


class UpdateStuffModel(BaseModel):
    '''Update Model Item'''
    name: Optional[str]
    description: Optional[str]
    categories: List[str] = []


@app.post('/', response_description='Create item', response_model=StuffModel)
async def create_item(item: StuffModel = Body(...)):
    item = jsonable_encoder(item)
    new_item = await db['itens'].insert_one(item)
    created_item = await db['itens'].find_one({'_id':new_item.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item)
