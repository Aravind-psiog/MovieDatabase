import os

from motor import motor_asyncio


async def get_database():
    """
    Get Database
    ----------------

    This function will fetch database name from the environment

    Args: None

    Returns: Name of the MongoDB name
    """
    mongo_db_name = os.environ.get("db_name")
    return mongo_db_name


async def get_client():
    """
    Get Client
    ----------------

    This function will fetch database client for the mongoDB

    Args: None

    Returns: Motor client for the MongoDB
    """
    mongo_user = os.environ.get("db_username")
    mongo_password = os.environ.get("db_password")
    mongo_url = os.environ.get("db_url")
    mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_url}"
    client = motor_asyncio.AsyncIOMotorClient(mongo_uri)
    return client


async def movies_motor_client():
    client = await get_client()
    db = client.theMovieDb
    movies_aggregation = db.get_collection('movies')
    return movies_aggregation


async def series_motor_client():
    client = await get_client()
    db = client.theMovieDb
    series_aggregation = db.get_collection('users')
    return series_aggregation
