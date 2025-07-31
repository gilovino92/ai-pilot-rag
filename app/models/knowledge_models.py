from pydantic import BaseModel
from typing import Optional

class RetrievalInput(BaseModel):
    knowledge_id: Optional[str] = None
    query: str
    retrieval_setting: Optional[dict] = None