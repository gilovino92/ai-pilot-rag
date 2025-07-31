from typing import Optional
from openai import OpenAI
from app.core.config import settings


class OpenAIAgent:
    _instance: Optional["OpenAIAgent"] = None
    _client: Optional[OpenAI] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIAgent, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            api_key = settings.AGENT_API_KEY
            if not api_key:
                raise ValueError("AGENT_API_KEY setting is not configured")
            self._client = OpenAI(
                api_key=api_key,
                timeout=30.0,  # 30 seconds timeout
                max_retries=3,  # Retry failed requests up to 3 times
            )

    @property
    def client(self) -> OpenAI:
        return self._client

    def get_client(self) -> OpenAI:
        return self.client 