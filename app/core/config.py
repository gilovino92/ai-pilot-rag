import warnings
from typing import Annotated, Any, Literal
import os

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    PORT: int = os.getenv("PORT", 8000)
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    API_KEY: str = "changethis"  # API key for authentication

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    # Weaviate settings
    WEAVIATE_URL: str
    WEAVIATE_API_KEY: str = ""

    # AI Agent settings
    AGENT_API_KEY: str = ""
    AI_AGENT_PROVIDER: Literal["openai", "ai_tool"] = "openai"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"


    # S3 settings
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_S3_BUCKET: str

    # Weaviate settings
    GENERAL_KNOWLEDGE_COLLECTION_NAME: str
    TENANT_KNOWLEDGE_COLLECTION_NAME: str

    # Tenant settings
    TENANT_URL: str
    TENANT_API_KEY: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret("WEAVIATE_API_KEY", self.WEAVIATE_API_KEY)
        self._check_default_secret("AGENT_API_KEY", self.AGENT_API_KEY)
        self._check_default_secret("API_KEY", self.API_KEY)
        return self

settings = Settings()  # type: ignore
