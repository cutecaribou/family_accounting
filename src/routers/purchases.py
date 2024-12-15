from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from src.models import Purchase, PurchaseWithID, PurchaseWithBuyer
import json
from src.db_session import engine, text
from src.routers.people import PeopleAPI

purchase_router = APIRouter(prefix="/purchases")

@cbv(purchase_router)
class PurchaseAPI:
    @purchase_router.get('/')
    def root(self, expand: bool = False):
        purchases_list = []
        with engine.connect() as con:
            query = text("""
                select id, purchase_date, amount, buyer_id
                from purchases
            """)
            result = con.execute(query)
            if expand:
                for row in result.mappings().all():
                    people = PeopleAPI()
                    certain_person = people.get_person(row['buyer_id'])
                    purchase = PurchaseWithBuyer(
                        purchase_id=row['id'],
                        purchase_date=row['purchase_date'],
                        amount=row['amount'],
                        buyer = certain_person
                    )
                    purchases_list.append(purchase)
            else:
                for row in result.mappings().all():
                    purchase = PurchaseWithID(
                        purchase_id = row['id'],
                        purchase_date = row['purchase_date'],
                        amount = row['amount'],
                        buyer_id = row['buyer_id']
                    )
                    purchases_list.append(purchase)
            con.close()
        return purchases_list

    @purchase_router.get('/{purchase_id}')
    def get_purchase(self, purchase_id: int, expand: bool = False):
        with engine.connect() as con:
            query = text("""
                select id, purchase_date, amount, buyer_id
                from purchases
                where id = (:purchase_id)
            """)
            result = con.execute(query, parameters={'purchase_id': purchase_id})
            try:
                row = result.mappings().one()
                if expand:
                    people = PeopleAPI()
                    certain_person = people.get_person(row['buyer_id'])
                    purchase = PurchaseWithBuyer(
                        purchase_id = row['id'],
                        purchase_date = row['purchase_date'],
                        amount = row['amount'],
                        buyer = certain_person
                    )
                else:
                    purchase = PurchaseWithID(
                        purchase_id = row['id'],
                        purchase_date = row['purchase_date'],
                        amount = row['amount'],
                        buyer_id = row['buyer_id']
                    )
                con.close()
            except Exception as e:
                print(e)
                purchase = None

            if purchase:
                return purchase
            else:
                raise HTTPException(status_code=404, detail="Purchase not found")


    @purchase_router.post('/')
    def create_new_purchase(self, purchase: Purchase):
        with engine.connect() as con:
            query = text("""
                insert into purchases
                (purchase_date, amount, buyer_id)
                values
                (:purchase_date, :amount, :buyer_id)
            """)
            con.execute(query, parameters={
                'purchase_date': purchase.purchase_date,
                'amount': purchase.amount,
                'buyer_id': purchase.buyer_id
            })
            con.commit()
            con.close()
        return json.loads(purchase.json())

    @purchase_router.delete('/{purchase_id}')
    def delete_by_id(self, purchase_id: int):
        with engine.connect() as con:
            query = text("""
                delete from purchases
                where id = (:purchase_id)
            """)
            con.execute(query, parameters={'purchase_id': purchase_id})
            con.commit()
            con.close()