from fastapi import APIRouter, Depends
from app.tool.ai_tool import get_ai_tool
from weaviate.classes.query import MetadataQuery
from app.core.weaviate_client import get_weaviate_client
from app.core.config import settings
from app.models.knowledge_models import RetrievalInput


router = APIRouter(prefix="/knowledge", tags=["knowledge"])

# @router.post("/query")
# async def query_from_general_knowledge(
#     data: RetrievalInput,
#     ai_tool=Depends(get_ai_tool)
# ):
#     """
#     Query knowledge with given knowledge_id and retrieval settings
    
#     Args:
#         knowledge_id: ID of the knowledge base to query
#         query: Query string
#         retrieval_setting: Optional settings for retrieval
#     """
#     try:
#         print(data)
#         db_dialect = get_db_dialect()
#         tables_info = await db_schema()
#         agent_answer = await ai_tool.generate_sql_query(data.query, tables_info, db_dialect)
        
#         # Extract SQL query string
#         sql_query = str(agent_answer).replace("\n", " ")
#         if "```sql" in sql_query:
#             sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
#         elif "```" in sql_query:
#             sql_query = sql_query.split("```")[1].strip()

#         # Execute query
#         query_result = await execute_query(sql_query)

#         return {
#             "status": "ok",
#             "knowledge_id": data.knowledge_id,
#             "agent_answer": agent_answer,
#             "sql_query": sql_query,
#             "content": query_result,
#             "retrieval_setting": data.retrieval_setting
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

@router.post("/retrieval")
async def general_knowledge_retrieval(retrieval_input: RetrievalInput = None):
    """
    Endpoint for general knowledge retrieval
    """
    weaviate_client = get_weaviate_client();
    try:
        ai_tool = get_ai_tool();
        tenant_collection = weaviate_client.collections.get(settings.TENANT_KNOWLEDGE_COLLECTION_NAME)
        # Set default retrieval settings if not provided
        if not retrieval_input.retrieval_setting:
            retrieval_input.retrieval_setting = {
                "top_k": 10,
                "score_threshold": 0.4
            }
        
        # Perform the search query
        embeddings = await ai_tool.get_embeddings(retrieval_input.query);
        results = tenant_collection.query.near_vector(
            near_vector=embeddings,
            limit=retrieval_input.retrieval_setting.get("top_k", 10),
            return_metadata=MetadataQuery(distance=True)
        );
        
        # Filter results based on score threshold
        filtered_results = []   
        for result in results.objects:
            # Convert distance to similarity score (1 - distance)
            similarity_score = 1 - result.metadata.distance
            if similarity_score >= retrieval_input.retrieval_setting.get("score_threshold", 0.4):
                filtered_results.append({
                    "content": result.properties.get("content", ""),
                    "title": result.properties.get("source", ""),
                    "metadata": {
                        "score": similarity_score
                    }
                })
        
        return filtered_results
        
    except Exception as e:
        print(f"Error retrieving knowledge: {str(e)}")
        raise
    finally:
        weaviate_client.close();
