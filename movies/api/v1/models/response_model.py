from typing import Optional, Union

from pydantic import BaseModel


class MoviesResponse(BaseModel):
    total_count: int
    results: Optional[list] = None


class MovieResponse(BaseModel):
    result: Optional[dict] = None
