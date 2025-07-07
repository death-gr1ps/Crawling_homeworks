from http import HTTPStatus
from os import getenv
from typing import Annotated, Any, Mapping

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
import pymongo
from pymongo.asynchronous.collection import AsyncCollection


class Book(BaseModel):
    title: str
    author: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price_amount: int | None = Field(default=None)
    price_currency: str | None = Field(default=None)
    rating_value: float | None = Field(default=None)
    rating_count: int | None = Field(default=None)
    publication_year: int
    isbn: str
    pages_cnt: int | None = Field(default=None)
    publisher: str | None = Field(default=None)
    book_cover: str | None = Field(default=None)
    source_url: str


app = FastAPI(title="Book ISBN Search Service", description="Study Case Example")


async def get_mongo_db() -> AsyncCollection[Mapping[str, Any] | Any]:
    mongo_uri = getenv("MONGO_URI")
    mongo_db = getenv("MONGO_DATABASE", "scrapy_data")
    mongo_db_collection = getenv("MONGO_DATABASE_COLLECTION", "scrapy_items")
    client = pymongo.AsyncMongoClient(mongo_uri)
    return client[mongo_db][mongo_db_collection]


@app.get("/search_by_isbn", tags=["ISBN Searcher"])
async def get_book_by_isbn(
    mongo_db: Annotated[AsyncCollection[Mapping[str, Any] | Any], Depends(get_mongo_db)],
    isbn: str,
) -> Book:
    result = await mongo_db.find_one({"isbn": isbn})
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Can't find book with this ISBN",
        )
    return Book(**result)

# fastapi dev api_server.py