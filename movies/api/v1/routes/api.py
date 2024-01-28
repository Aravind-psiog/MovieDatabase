from fastapi import APIRouter

from movies.api.v1.endpoints import movies

router = APIRouter()

router.include_router(movies.router, tags=["movies"])
