from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from models import Person, PersonWithID
import json
from db_session import engine, text

people_router = APIRouter(prefix="/people")


@cbv(people_router)
class PeopleAPI:
    @people_router.get('/')
    def root(self):
        persons_list = []
        with engine.connect() as con:
            query = text("""
                       select id, name, is_parent
                        from people
                   """)
            result = con.execute(query)
            for row in result.mappings().all():
                person = PersonWithID(
                    person_id = row['id'],
                    name = row['name'],
                    is_parent = row['is_parent']
                )
                persons_list.append(person)
            con.close()
        return persons_list

    @people_router.get('/{person_id}')
    def get_person(self, person_id: int):
        with engine.connect() as con:
            query = text("""
                select id, name, is_parent
                from people
                where id = (:person_id)
            """)
            result = con.execute(query, parameters={'person_id': person_id})
            try:
                row = result.mappings().one()
                person = PersonWithID(
                    person_id=row['id'],
                    name=row['name'],
                    is_parent=row['is_parent']
                )
            except:
                person = None
            con.close()
        if person:
            return person
        else:
            raise HTTPException(status_code=404, detail="Person not found")


    @people_router.post('/')
    def create_new_person(self, person: Person):
        with engine.connect() as con:
            query = text("""
                insert into people
                (name, is_parent)
                values
                (:name, :is_parent)
            """)
            con.execute(query, parameters={
                'name': person.name,
                'is_parent': person.is_parent
            })
            con.commit()
            con.close()
        return json.loads(person.json())


    @people_router.delete('/{person_id}')
    def delete_by_id(self, person_id: int):
        with engine.connect() as con:
            query = text("""
                delete from people
                where id = (:person_id)
            """)
            con.execute(query, parameters={'person_id': person_id})
            con.commit()
            con.close()

