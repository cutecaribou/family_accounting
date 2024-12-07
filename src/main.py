import sqlalchemy as sq
import json
from fastapi import FastAPI


def connect(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)

    # print(json.dumps(data, indent=4))
    url = 'postgresql+psycopg2://{login}:{password}@{host}:{port}/{database}'
    url = url.format(**data['connection'])
    engine = sq.create_engine(url)

    with engine.connect() as con:
        query = sq.text('select version() as v')
        res = con.execute(query)
        for row in res.mappings().all():
            # print(row)
            print(row['v'])
        con.close()

    return engine


def main():
    engine = connect('settings.json')
    app = FastAPI()

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
