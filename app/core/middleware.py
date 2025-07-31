from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip API key check for OpenAPI documentation and health check
        if request.url.path in ["/api/v1/openapi.json", "/api/v1/docs", "/api/v1/redoc", "/api/v1/utils/health-check/"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Authorization header is missing. Please provide it as 'Bearer {API_KEY}'."
            )
        
        try:
            # Check if the header starts with "Bearer "
            if not auth_header.startswith("Bearer "):
                raise ValueError("Invalid authorization header format")
            
            # Extract the token part
            api_key = auth_header.split(" ")[1]
            
            if not api_key:
                raise ValueError("API key is missing")
            
            if api_key != settings.API_KEY:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid API key."
                )
            
            return await call_next(request)
            
        except ValueError as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            ) 