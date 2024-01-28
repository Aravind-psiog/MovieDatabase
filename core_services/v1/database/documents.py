import datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID, uuid4

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field, constr


class Movies(Document):

    id: PydanticObjectId
    original_title: str
    original_language: str
    overview: str
    popularity: float
    vote_average: float
    vote_count: float
    title: str
    generes: list[str] = []
    release_date: Optional[datetime.datetime]
    backdrop_url: Optional[str] = None
    poster_url: Optional[str] = None

    class Settings:
        """
        Settings
        ---------

        Configuration of model class for Movies collection

        Attributes:
            name: Name of the collection
            validate_on_save: Config to save the collection values on save
        """

        name = "movies"
        validate_on_save = True


class User(Document):

    id: PydanticObjectId
    comments: Optional[list]
    email: str
    username: str
    favourite: Optional[list]

    class Settings:
        """
        Settings
        ---------

        Configuration of model class for Movies collection

        Attributes:
            name: Name of the collection
            validate_on_save: Config to save the collection values on save
        """

        name = "users"
        validate_on_save = True

