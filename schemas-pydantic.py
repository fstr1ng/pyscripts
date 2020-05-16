from enum import Enum
from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, ValidationError, validator


class Category(BaseModel):
    name: str = Field(max_length=128)
    description: str = Field(max_length=1024)

    @validator('name')
    def must_be_uniq(cls, value):
        if value in ['Shells']:
            raise ValueError(f'"{value}" already exists in db')
        return value

class CategoryOut(Category):
    id: ObjectId = Field(alias='_id')
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }

class Policy(BaseModel):
    updated: datetime = Field(default_factory=datetime.now)

schemas = {
       'category':  {'in': Category,  'out': CategoryOut},
    #  'policy':    {'in': Policy,    'out': PolicyOut},
    #  'file':      {'in': File,      'out': File},
    #  'signature': {'in': Signature, 'out': Signature},
    #  'subsign':   {'in': Subsign,   'out': Subsign},
    #  'option':    {'in': Option,    'out': Option},
    }

#print(Category(name='Shells', description='AAA'))
