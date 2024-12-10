from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from models import Person
import json

people_router = APIRouter(prefix="/people")

@cbv(people_router)
class PeopleAPI:
    @people_router.get('/')
    def root(self):
        return 'gets all people'

    @people_router.get('/{person_id}')
    def get_person(self, person_id: int):
        return f'gets a certain people {person_id}'
        # return

    @people_router.post('/')
    def create_new_person(self, person: Person):
        return json.loads(person.json())

