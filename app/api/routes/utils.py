from fastapi import APIRouter
from typing import List, Optional, Union
from pydantic import BaseModel
from app.tool.vectorDB_tool import get_vector_record_by_filters

router = APIRouter(prefix="/utils", tags=["utils"])


class TableNameRequest(BaseModel):
    table_name: str


class FilterCondition(BaseModel):
    path: Union[str, List[str]]
    operator: str
    value: Union[str, int, float, bool, List[str], List[int], List[float], List[bool]]


class KnowledgeFilterRequest(BaseModel):
    filters: Union[FilterCondition, List[FilterCondition]]
    limit: Optional[int] = 10


@router.post("/knowledge-by-filters")
async def filter_knowledge(request: KnowledgeFilterRequest):
    """
    Retrieve vector records using filters.
    
    Example request body:
    {
        "filters": [
            {
                "path": ["source"],
                "operator": "Equal",
                "value": "document1"
            },
            {
                "path": ["knowledge_type"],
                "operator": "Equal",
                "value": "text"
            }
        ],
        "limit": 10
    }
    """
    try:
        # Convert filter conditions to Weaviate Filter objects
        filters_list = [request.filters] if isinstance(request.filters, FilterCondition) else request.filters

        results = await get_vector_record_by_filters(
            filters=filters_list,
            limit=request.limit
        )
        
        return {
            "status": "success",
            "count": len(results),
            "items": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/health-check/")
async def health_check() -> bool:
    return True