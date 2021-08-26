import os
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from bson import ObjectId
import motor.motor_asyncio


app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGODB_URL'])  # Set with export in .env
db = client.stuff  # Set client to the Stuff Collection


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
    id = PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)
    description: Optional[str] = None
    categories: List[str] = []


class UpdateStuffModel(BaseModel):
    '''Update Model Item'''
    name: Optional[str]
    description: Optional[str]
    categories: List[str] = []
