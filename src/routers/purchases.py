from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from src.models import Purchase, PurchaseWithID
import json
from src.db_session import engine, text

purchase_router = APIRouter(prefix="/purchases")

@cbv(purchase_router)
class PurchaseAPI:
    @purchase_router.get('/')
    def root(self):
        purchases_list = []
        with engine.connect() as con:
            query = text("""
                select id, purchase_date, amount, buyer_id
                from purchases
            """)
            result = con.execute(query)
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