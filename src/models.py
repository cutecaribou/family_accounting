from pydantic import BaseModel


class Person(BaseModel):
    name: str
    is_parent: bool
