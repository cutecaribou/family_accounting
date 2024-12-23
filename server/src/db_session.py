import sqlalchemy as sq
import json

from sqlalchemy import text

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


engine = connect('settings.json')