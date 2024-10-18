from core_services.v1.database.documents import Movies, User
from core_services.v1.database import database
from beanie import init_beanie
from fastapi import Depends, FastAPI, Request, APIRouter
from core_services.v1.services import config_service, resource
from starlette.middleware.cors import CORSMiddleware
import movies.api.v1.routes.api as movies_route
import series.api.v1.routes.api as series_route
from mangum import Mangum

lambdaPaths = resource.resources()

if lambdaPaths["staging"] is None:
    fastapi_doc = None
else:
    fastapi_doc = f'{lambdaPaths["staging"]}'

app = FastAPI(root_path=fastapi_doc)
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    """
    Add Cors Header
    ---------------

    This function will add CORS headers to HTTP responses

    Args:
        request (Request): The incoming HTTP request object
        call_next: A callable representing the next middleware or route handler in the chain.

    Returns:
        Response: The HTTP response object with added CORS headers
    """
    response = await call_next(request)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


@app.on_event("startup")
async def startup_event():
    """
    Startup Event
    ---------------

    This function will act as an handler for the startup phase for the main application

    Args: None

    Returns: None
    """
    config_service.load_config()
    client = await database.get_client()
    db = await database.get_database()
    await init_beanie(
        database=client[db],
        document_models=[
            Movies,
            User
        ],
    )


@router.get("/")
async def default():
    return {"message": "visit /docs for swagger"}

app.include_router(router)
app.include_router(movies_route.router)
app.include_router(series_route.router)
handler = Mangum(app, api_gateway_base_path=lambdaPaths["resource"])
