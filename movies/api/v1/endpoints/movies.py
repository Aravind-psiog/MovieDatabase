from typing import Optional
import datetime
from beanie import PydanticObjectId

from fastapi import APIRouter, Query, HTTPException
from pydantic import conint
from pyparsing import empty
from typing import Any, Union
from fastapi.encoders import jsonable_encoder
from core_services.v1.database.documents import Movies, User

from core_services.v1.database.database import series_motor_client, movies_motor_client
from movies.api.v1.models.request_models import Language, SortBy, SortDirection
from movies.api.v1.models.response_model import MoviesResponse, MovieResponse
from movies.api.v1.services.movie_services import (list_movie_service,
                                                   get_movies_count, global_search_movies,
                                                   language_search_movies, get_movie_detail)
from bson import ObjectId
from pydantic import BaseModel, Field

router = APIRouter()


class CustomObjectIdField:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> str:
        if isinstance(value, ObjectId):
            return str(value)
        return value


class YourModel(BaseModel):
    _id: Union[ObjectId, str, CustomObjectIdField]
    adult: bool
    ref_id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    release_date: Optional[datetime.datetime]
    title: str
    video: bool
    vote_average: float
    vote_count: int
    generes: list
    backdrop_url: Optional[str]
    poster_url: Optional[str]
    title_search: str


@router.get("/count")
async def movies_count():
    count = await get_movies_count()
    return {"count": count}


@router.get("/movies", response_model=MoviesResponse)
async def list_movies(
    count: Optional[conint(gt=0, le=100)] = Query(10),
    page: Optional[conint(gt=0)] = Query(),
    language: Optional[Language] = None,
    sort: Optional[SortBy] = SortBy.POPULARITY,
    direction: Optional[SortDirection] = SortDirection.DESCENDING,
    search: Optional[str] = "",
):
    page = page*count
    sort = SortBy[sort.name].value
    if search:
        if language:
            count, result = await language_search_movies(language, sort, direction, page, count, search)
            return MoviesResponse(total_count=len(count), results=result)
        count, result = await global_search_movies(sort, direction, page, count, search)
        return MoviesResponse(total_count=len(count), results=result)
    movies = await list_movie_service(language, sort, direction, page, count)
    return MoviesResponse(total_count=await get_movies_count(), results=movies)


@router.get("/movie", response_model=MovieResponse)
async def get_a_movie(
    _id: str
):
    try:
        PydanticObjectId(_id)
    except:
        raise HTTPException(status_code=422, detail=f"Invalid item id {_id}")
    movie = await get_movie_detail(_id)
    if movie:
        return MovieResponse(result=jsonable_encoder(movie))
    raise HTTPException(status_code=404, detail=f"Movie {_id} not found")


@router.get("/favourites")
async def get_favourites(ref_id: str):
    import requests
    import uuid
    import boto3
    from botocore.exceptions import NoCredentialsError
    import pymongo
    import os
    from bson import ObjectId
    from datetime import datetime
    from bson import ObjectId

    uri = "mongodb+srv://Aravind:6Sw8EBzrgw3F8JyN@moviedb.wqounyl.mongodb.net/"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyOGM3YzY1M2QwZDk5Y2VhN2Q2ZGFhMzUwYzRiYjk0MyIsInN1YiI6IjYyMTYxOGQxMWEzMjQ4MDAxYzRmZjNiYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5BY5yQ_RAGRiihDNLu6gEOK-AI-o8Oc08zwkMjJjMEk"
    }

    myclient = pymongo.MongoClient(uri)
    from core_services.v1.database.documents import Movies
    mydb = myclient["theMovieDb"]
    temp_collection = mydb["temp_collection"]
    # movies = mydb["movies"]
    mv = await movies_motor_client()
    users = mydb['users']
    a = await series_motor_client()
    regex_pattern = "\\b" + "blue" + "\\b"
    pipeline = [
        {
            '$match': {
                '_id': ObjectId(ref_id)  # Filter by user _id (User 1)
            }},
        {
            '$lookup': {
                'from': 'movies',  # Primary collection name
                'localField': 'favourite_movies',  # Field in the secondary collection
                'foreignField': '_id',  # Field in the primary collection
                'as': 'joined_data'  # Alias for the merged documents
            }
        },

        {
            '$unwind': '$joined_data'  # Flatten the array
        },
        # {
        #     '$unwind': '$favorite_movies'  # Flatten the array
        # },
        {
            '$match': {
                # 'joined_data.original_language': 'en',    # Match the specific 'key'
                # Perform regex match on the 'value' field
                'joined_data.title_search': {'$regex': regex_pattern}
            }
        }

    ]

    # Execute the aggregation pipeline
    # result = list(users.aggregate(pipeline))
    # search_aggregate = [
    #     {
    #         "$search": {
    #             "compound": {
    #                 "should": [
    #                     {"autocomplete": {"query": "blue", "path": "title_search"}}
    #                 ]
    #             }
    #         }
    #     },
    #     {
    #         '$match': {
    #             # Filter by matching document IDs
    #             Movies.id: {'$in': result[0]['favorite_movies']}
    #         }},
    #     {"$addFields": {
    #         "_id": {"$toString": "$_id"}
    #     }}

    # ]
    search_result = await User.find().aggregate(pipeline).to_list()
    # print(search_result[0]['joined_data'])

    # Print the enriched collection2 documents with all data from collection1
    for doc in search_result:
        data = doc["joined_data"]
        a = YourModel(**data)
        print(a)
    return {"mess": "gl"}
