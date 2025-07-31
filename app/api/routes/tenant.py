import asyncio
from io import BytesIO
from turtle import pd
from PyPDF2 import PdfReader
from docx import Document
from sqlalchemy import inspect
from fastapi import APIRouter, File, HTTPException, Path, Depends, UploadFile, Body
from typing import Optional
from pydantic import BaseModel
from app.controllers.tenant_controller import upload_knowledge, get_tenant_object_by_tenant_id, retrieve_knowledge, process_knowledge_from_s3_object
from app.tool.ai_tool import get_ai_tool
from app.models.knowledge_models import RetrievalInput
from app.tool.vectorDB_tool import delete_vector_record_with_tenant_id

router = APIRouter(prefix="/tenant", tags=["tenant"])

class UploadKnowledgeRequest(BaseModel):
    knowledge_id: str



# @router.post("/upload-knowledge")
# async def upload_knowledge_endpoint(
#     knowledge_id: str = Body(..., description="The ID of the knowledge base"),
#     file: UploadFile = File(..., description="File to upload (TXT, MD, PDF, etc. Max 15MB)")
# ):
#     """
#     Endpoint for uploading knowledge from supported file types
#     Supports: TXT, MARKDOWN, MDX, PDF, HTML, XLSX, XLS, DOCX, CSV, MD, HTM
#     Maximum file size: 15MB
#     """
#     try:
#         # Validate file size (15MB limit)
#         file_content = await file.read()
#         if len(file_content) > 15 * 1024 * 1024:  # 15MB in bytes
#             raise HTTPException(status_code=400, detail="File size exceeds 15MB limit")

#         # Validate file extension
#         allowed_extensions = ['.txt', '.md', '.mdx', '.pdf', '.html', '.xlsx', 
#                             '.xls', '.docx', '.csv', '.htm', '.markdown']
#         print(file.filename);

#         file_ext = file.filename[file.filename.rfind('.'):].lower()
#         if file_ext not in allowed_extensions:
#             raise HTTPException(status_code=400, 
#                               detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}")

#         # Read file content based on type
#         content = ""
#         if file_ext in ['.txt', '.md', '.mdx', '.markdown', '.htm', '.html']:
#             content = file_content.decode('utf-8')
#         elif file_ext == '.pdf':
#             # Use PyPDF2 or similar to extract text
#             reader = PdfReader(BytesIO(file_content))
#             content = " ".join([page.extract_text() for page in reader.pages])
#         elif file_ext in ['.xlsx', '.xls']:
#             # Use pandas to read Excel
#             df = pd.read_excel(BytesIO(file_content))
#             content = df.to_string()
#         elif file_ext == '.docx':
#             # Use python-docx to read Word docs
#             doc = Document(BytesIO(file_content))
#             content = " ".join([paragraph.text for paragraph in doc.paragraphs])
#         elif file_ext == '.csv':
#             # Use pandas to read CSV
#             df = pd.read_csv(BytesIO(file_content))
#             content = df.to_string()

#         # Upload the extracted content
#         asyncio.run(upload_knowledge(knowledge_id, content, source=file.filename))
#         return {
#             "message": "File uploaded and processed successfully",
#             "knowledge_id": knowledge_id,
#             "filename": file.filename,
#         }
#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         return {"error": str(e)}

@router.post("/objects")
async def get_tenant_objects(
    knowledge_id: str = Body(..., description="The ID of the knowledge base")
):
    """
    Endpoint to retrieve all objects associated with a knowledge base
    """
    try:
      results = await get_tenant_object_by_tenant_id(knowledge_id);
      return {
          "knowledge_id": knowledge_id,
          "objects": results
      }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieval")
async def retrieve_knowledge_endpoint(
    request: RetrievalInput,
):
    """
    Retrieve vector records from a specific knowledge base
    """
    try:
        results = await retrieve_knowledge(
            tenant_id=request.knowledge_id,
            query=request.query,
            top_k=request.retrieval_setting.get("top_k", 10),
            score_threshold=request.retrieval_setting.get("score_threshold", 0.4),
        )
        return {
            "results": results,
        }
    except Exception as e:
        print(e);
        return {
            "results": []
        }

@router.post("/upload-knowledge")
async def get_documents(
    tenant_id: str = Body(..., description="The ID of the knowledge base"),
    key: str = Body(..., description="The name of the file to retrieve"),
):
    """ 
    Endpoint to retrieve all documents associated with a knowledge base
    """
    try:
        process_knowledge_from_s3_object(tenant_id, key);
        return {
            "data": "Started processing uploaded knowledge"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/knowledge/{tenant_id}")
async def delete_knowledge(
    tenant_id: str = Path(..., description="The ID of the knowledge base"),
):
    """ 
    Endpoint to delete a knowledge base
    """
    try:
        print(f'Deleting knowledge base with tenant id: {tenant_id}');
        result = await delete_vector_record_with_tenant_id(tenant_id);
        return {
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
