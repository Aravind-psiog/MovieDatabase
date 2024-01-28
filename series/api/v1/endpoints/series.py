from beanie import Document
from fastapi import APIRouter, HTTPException, Query, Request
from core_services.v1.database.documents import Movies
from movies.api.v1.models.request_models import Language, SortBy, SortDirection
from movies.api.v1.models.response_model import MovieResponse

from pydantic import BaseModel, Field, model_validator
from bson import ObjectId
from typing import Optional
from pydantic import conint
from pyparsing import empty

router = APIRouter()
