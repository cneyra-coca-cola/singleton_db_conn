from fastapi import Header, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv, dotenv_values
import os

from app.api.models import MovieIn, MovieOut
from app.db.db_singleton import DatabaseClient
from app.db.schemas import movies_table

movies = APIRouter()

# Loading variables from .env file
load_dotenv()

# Load Local Variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_table = os.getenv("DB_TABLE")

database_manager = DatabaseClient(user=db_user, password=db_password, table=db_table)


# Background task to close the database connection
async def close_database_connection():
    await database_manager.shutdown()


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn, background_task: BackgroundTasks):
    query = movies_table.insert().values(**payload.dict())

    # Database startup
    await database_manager.startup()

    # Schedule the shutdown task
    background_task.add_task(close_database_connection)

    # Execute the query and return the result
    return await database_manager.execute(query=query)
