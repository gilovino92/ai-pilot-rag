from app.core.weaviate_client import get_weaviate_client
from weaviate.classes.tenants import Tenant
from app.core.config import settings
from app.utils.helpers import split_content_into_chunks
from app.tool.vectorDB_tool import store_vector_record_with_tenant_id
from app.tool.ai_tool import get_ai_tool
from weaviate.classes.query import MetadataQuery
from app.tool.s3 import process_s3_object
import asyncio
import threading


async def check_tenant_exists(client, tenant_id: str):
    collection = client.collections.get(settings.TENANT_KNOWLEDGE_COLLECTION_NAME)
        # List all tenants
    tenants = collection.tenants.get()
    tenant_names = [tenant for tenant in tenants]
    
    # Check if tenant exists
    if tenant_id not in tenant_names:
        return False;
    return True;

async def ensure_tenant_exists(client, tenant_id: str):
    """Check if tenant exists and create it if it doesn't."""
    try:
        # Get the collection
        collection = client.collections.get(settings.TENANT_KNOWLEDGE_COLLECTION_NAME)
        
        # List all tenants
        tenants = collection.tenants.get()
        tenant_names = [tenant for tenant in tenants]
        
        # Check if tenant exists
        if tenant_id not in tenant_names:
            print(f"Creating tenant: {tenant_id}")
            # Create the tenant
            collection.tenants.create(
                tenants=[
                    Tenant(name=tenant_id),
                ]
            )
            print(f"Tenant {tenant_id} created successfully")
        else:
            print(f"Tenant {tenant_id} already exists")
            
    except Exception as e:
        print(f"Error ensuring tenant exists: {str(e)}")
        raise


async def upload_knowledge(tenant_id: str, content: str, source: str):
    # Split content into chunks of approximately 500 tokens
    chunks = split_content_into_chunks(content,source);
    store_vector_record_with_tenant_id(chunks, tenant_id, settings.TENANT_KNOWLEDGE_COLLECTION_NAME);
    return True;


async def get_tenant_object_by_tenant_id(tenant_id: str):
    weaviate_client = get_weaviate_client();
    tenant_collection = weaviate_client.collections.get(settings.TENANT_KNOWLEDGE_COLLECTION_NAME).with_tenant(tenant_id);
    # Split content into chunks of approximately 500 tokens
    results = tenant_collection.query.fetch_objects();
    return results;


async def retrieve_knowledge(tenant_id: str, query: str, top_k: int = 10, score_threshold: float = 0.4):
    """
    Retrieve vector records from a specific tenant's knowledge base
    """
    weaviate_client = get_weaviate_client();
    try:
        ai_tool = get_ai_tool();
        
        tenant_exists = await check_tenant_exists(weaviate_client, tenant_id);
        if(tenant_exists == False):
            return [];
        tenant_collection = weaviate_client.collections.get(settings.TENANT_KNOWLEDGE_COLLECTION_NAME).with_tenant(tenant_id)
        print(tenant_collection);
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
        return [];
    finally:
        weaviate_client.close();
        print('\033[41m\033[30mweaviate client closed \033[0m');



def run_async_in_thread(loop: asyncio.AbstractEventLoop, coro):
    """Run an async coroutine in a new thread."""
    asyncio.set_event_loop(loop)  # Set the event loop for the thread
    loop.run_until_complete(coro)
    loop.close()

def process_knowledge_from_s3_object(tenant_id: str, key: str):
    # Create a new event loop for the thread
    new_loop = asyncio.new_event_loop()

    # Create the async task
    coro = process_s3_object(tenant_id, key)

    # Run the async task in a new thread
    thread = threading.Thread(target=run_async_in_thread, args=(new_loop, coro))
    thread.start()


# Check/create tenant

