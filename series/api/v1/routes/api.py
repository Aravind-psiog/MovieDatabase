from fastapi import APIRouter
from series.api.v1.endpoints import series

router = APIRouter()

router.include_router(series.router, tags=["series"])
