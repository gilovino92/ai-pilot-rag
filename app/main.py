from contextlib import asynccontextmanager
from app.core import weaviate_client
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings
from app.core.middleware import APIKeyMiddleware
from app.core.weaviate_client import create_required_collections
def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)
# Lifespan event to manage Weaviate client connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_required_collections();
    yield

app = FastAPI(lifespan=lifespan)


# Add API key middleware
app.add_middleware(APIKeyMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    port = int(settings.PORT) if hasattr(settings, 'PORT') else 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)