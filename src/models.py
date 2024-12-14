from pydantic import BaseModel


class Person(BaseModel):
    name: str
    is_parent: bool


class PersonWithID(Person):
    person_id: int
