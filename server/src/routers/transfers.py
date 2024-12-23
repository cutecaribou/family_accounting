from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from src.models import Transfer, TransferWithID
import json
from src.db_session import engine, text



transfer_router = APIRouter(prefix="/transfers")

@cbv(transfer_router)
class TransferAPI():
    @transfer_router.get('/')
    def root(self):
        transfers_list = []
        with engine.connect() as con:
            query = text("""
                select id, transfer_date, amount, purchase_id, target_id, source_id
                from transfers
            """)
            result = con.execute(query)
            for row in result.mappings().all():
                transfer = TransferWithID(
                    transfer_id = row['id'],
                    transfer_date = row['transfer_date'],
                    amount = row['amount'],
                    purchase_id = row['purchase_id'],
                    target_id = row['target_id'],
                    source_id = row['source_id']
                )
                transfers_list.append(transfer)
            con.close()

        return transfers_list


    @transfer_router.post('/')
    def create_new_transfer(self, transfer: Transfer):
        with engine.connect() as con:
            query = text("""
                insert into transfers
                (transfer_date, amount, purchase_id, target_id, source_id)
                values
                (:transfer_date, :amount, :purchase_id, :target_id, :source_id)
            """)
            con.execute(query, parameters={
                'transfer_date': transfer.transfer_date,
                'amount': transfer.amount,
                'purchase_id': transfer.purchase_id,
                'target_id': transfer.target_id,
                'source_id': transfer.source_id
            })
            con.commit()
            con.close()
            return json.loads(transfer.json())