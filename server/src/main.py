from src.db_session import engine
import sqlalchemy as sq
from fastapi import FastAPI
from src.routers.people import people_router
from src.routers.purchases import purchase_router
from src.routers.transfers import transfer_router


def main():
    app = FastAPI()
    app.include_router(people_router)
    app.include_router(purchase_router)
    app.include_router(transfer_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/version")
    async def version():
        with engine.connect() as con:
            query = sq.text('select version() as v')
            res = con.execute(query)
            for row in res.mappings().all():
                bd_version = row['v']
            con.close()
        return {
            "bd": bd_version,
            "server": "0.0.1"
        }

    return app


# if __name__ == '__main__':
app = main()
