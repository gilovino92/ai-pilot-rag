import httpx
from app.core.config import settings

async def update_document_status(key: str, status: str) -> dict:
    """
    Update tenant document status from Tenant service using API key.
    
    Args:
        tenant_id: ID of the tenant to retrieve
        
    Returns:
        Dict containing tenant information or None if not found
    """
    headers = {
        "x-api-key": settings.TENANT_API_KEY
    }
    print(f"Updating document status for {key} to {status}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.TENANT_URL}/tenant-backend/v1/internal/customers/update-org-document",
                headers=headers,
                json={
                    "key": key,
                    "status": status
                }
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                raise Exception(f"Failed to get tenant info: {response.text}")
                
    except Exception as e:
        print(f"Error calling tenant service: {str(e)}")
        return None