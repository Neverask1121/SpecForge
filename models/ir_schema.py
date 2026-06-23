from pydantic import BaseModel
from typing import List


class Field(BaseModel):
    name: str
    type: str
    required: bool


class Entity(BaseModel):
    name: str
    fields: List[Field]


class Permission(BaseModel):
    role: str
    feature: str
    permission: str


class Relationship(BaseModel):
    source: str
    target: str
    relation_type: str


class Workflow(BaseModel):
    name: str
    steps: List[str]


class IR(BaseModel):
    app_name: str
    entities: List[Entity]
    roles: List[str]
    permissions: List[Permission]
    relationships: List[Relationship]
    workflows: List[Workflow]