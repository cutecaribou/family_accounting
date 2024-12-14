from pydantic import BaseModel
from datetime import date


class Person(BaseModel):
    name: str
    is_parent: bool


class PersonWithID(Person):
    person_id: int

class Purchase(BaseModel):
    purchase_date: date
    amount: int
    buyer_id: int


class PurchaseWithID(Purchase):
    purchase_id: int