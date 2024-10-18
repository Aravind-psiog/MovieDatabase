from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CreateMovies(BaseModel):
    title: str
    description: str = None
    year: int


@app.post("/movies/")
async def create_item(item: CreateMovies):
    # Logic to create item
    return {"item_name": item.title, "item_description": item.description, "item_price": item.year}
