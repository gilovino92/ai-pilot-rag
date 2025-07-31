from app.tool.ai_tool import get_ai_tool
from app.core.weaviate_client import get_weaviate_client
from weaviate.classes.query import MetadataQuery
from app.core.config import settings

async def retrieve_vector_record(query: str, top_k: int = 10, score_threshold: float = 0.4):
    """
    Retrieve vector records from the general knowledge base
    """
    try:
        ai_tool = get_ai_tool();
        weaviate_client = await get_weaviate_client()
        tenant_collection = weaviate_client.collections.get(settings.GENERAL_KNOWLEDGE_COLLECTION_NAME)
        
        # Perform the search query
        embeddings = await ai_tool.get_embeddings(query);
        results = tenant_collection.query.near_vector(
            near_vector=embeddings,
            limit=top_k,
            return_metadata=MetadataQuery(distance=True)
        );
        
        # Filter results based on score threshold
        filtered_results = []
        for result in results.objects:
            # Convert distance to similarity score (1 - distance)
            similarity_score = 1 - result.metadata.distance
            if similarity_score >= score_threshold:
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