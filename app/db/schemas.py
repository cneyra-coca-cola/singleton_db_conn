from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

metadata = MetaData()

movies_table = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts', ARRAY(String))
)
