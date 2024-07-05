from sqlalchemy import (MetaData, create_engine)
from databases import Database


class DataBaseClient:
    user: str
    password: str
    table: str

    def __init__(self, user, password, table):
        self.user = user
        self.password = password
        self.table = table

        self.connection_url = f"postgresql://{user}:{password}@localhost/{table}"
        self.database = Database(self.connection_url)
        self.engine = create_engine(self.connection_url)
        self.metadata = MetaData()

    async def startup(self):
        await self.database.connect()

    async def shutdown(self):
        await self.database.disconnect()

    async def execute(self, query):
        return await self.database.execute(query)


