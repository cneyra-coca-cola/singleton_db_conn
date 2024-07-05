from fastapi import FastAPI
from app.api.movies import movies
from app.api.db import metadata, engine

metadata.create_all(engine)

app = FastAPI()

app.include_router(movies)
