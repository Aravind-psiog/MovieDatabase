from pyparsing import empty


from core_services.v1.database.documents import Movies
from movies.api.v1.models.request_models import Language, SortBy, SortDirection


async def get_movies_count():
    return await Movies.count()


async def list_movie_service(language: str, sort: str, direction: str, offset: int, count: int):

    language_query = {}
    if language:
        language_query[Movies.original_language] = Language[language.name].value.lower()
    sort_direction = "+" if direction.name == SortDirection.ASCENDING.name else "-"
    movies = await Movies.find(language_query).sort(sort_direction+sort.lower()).skip(offset).limit(count).to_list()
    return movies


async def global_search_movies(sort, direction, offset, count, search):
    sort_direction = +1 if direction.name == SortDirection.ASCENDING.name else -1
    search_aggregate = [
        {
            "$search": {
                "compound": {
                    "should": [
                        {"autocomplete": {"query": search, "path": "title_search"}}
                    ]
                }
            }
        },
        {"$sort": {sort.lower(): sort_direction}},
        {"$addFields": {
            "_id": {"$toString": "$_id"}
        }}

    ]
    search_result = await Movies.find().aggregate(search_aggregate).to_list()
    return search_result, search_result[offset:count]


async def language_search_movies(language, sort, direction, offset, count, search):
    sort_direction = +1 if direction.name == SortDirection.ASCENDING.name else -1
    search_aggregate = [
        {
            "$search": {
                "compound": {
                    "should": [
                        {"autocomplete": {"query": search, "path": "title_search"}}
                    ]
                }
            }
        },
        {
            "$match": {
                Movies.original_language: Language[language.name].value.lower()
            },
        },
        {"$sort": {sort.lower(): sort_direction}},
        {"$addFields": {
            "_id": {"$toString": "$_id"}
        }}

    ]
    search_result = await Movies.find().aggregate(search_aggregate).to_list()
    return search_result, search_result[offset:count]


async def get_movie_detail(id):

    return await Movies.get(id)
