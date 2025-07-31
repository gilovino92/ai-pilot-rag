import weaviate
from app.core.config import settings
from weaviate.auth import Auth
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import Configure, Property, DataType

def get_weaviate_client():
    """Return the Weaviate client instance."""
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=settings.WEAVIATE_URL,
        auth_credentials=Auth.api_key(settings.WEAVIATE_API_KEY),
        skip_init_checks=True,
        additional_config=AdditionalConfig(
            timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
        ),
    )
    client.connect();
    print('\033[42m\033[30mweaviate client connected \033[0m');
    return client;

def create_required_collections():
    client = get_weaviate_client();
    try:
        collections = client.collections.list_all()
        collection_names = [collection for collection in collections]

        if settings.TENANT_KNOWLEDGE_COLLECTION_NAME not in collection_names:
            print(f"Creating collection: {settings.TENANT_KNOWLEDGE_COLLECTION_NAME}")
            # Create the collection with the specified settings
            client.collections.create(
                name=settings.TENANT_KNOWLEDGE_COLLECTION_NAME,
                vectorizer_config=Configure.Vectorizer.text2vec_openai(
                    model="text-embedding-3-small",
                        base_url="https://api.openai.com",
                        vectorize_collection_name=False,  # Equivalent to "Vectorize class name" being disabled
                    ),
                    properties=[
                        Property(
                            name="content", data_type=DataType.TEXT, vectorize=True
                        ),
                        Property(
                            name="knowledge_type",
                            data_type=DataType.TEXT,
                            vectorize=False,
                        ),
                        Property(
                            name="source", data_type=DataType.TEXT, vectorize=False
                        ),
                        Property(
                            name="metadata",
                            data_type=DataType.OBJECT,
                            vectorize=False,
                            nested_properties=[
                                Property(
                                    name="source_id", data_type=DataType.TEXT, vectorize=False
                                ),
                            ],
                        ),
                    ],
                    multi_tenancy_config=Configure.multi_tenancy(
                        enabled=True,
                        auto_tenant_creation=True
                    ),  # Multi-tenancy disabled
                )
            print(f"Collection {settings.TENANT_KNOWLEDGE_COLLECTION_NAME} created successfully")
        else:
            print(f"Collection {settings.TENANT_KNOWLEDGE_COLLECTION_NAME} already exists")

    except Exception as e:
        print(f"Error ensuring collections exist: {str(e)}")
        raise
    finally:
        client.close();
        print('\033[41m\033[30mweaviate client closed \033[0m');

# class WeaviateClientManager:
#     def __init__(self):
#         self.client = None
#         self.retry_count = 0
#         self.is_ready = False

#     async def connect(self):
#         print("Connecting to Weaviate")
#         """Initialize and connect the Weaviate client."""
#         try:
#             if(self.client is None):
#                 self.client = weaviate.connect_to_weaviate_cloud(
#                     cluster_url=settings.WEAVIATE_URL,
#                     auth_credentials=Auth.api_key(settings.WEAVIATE_API_KEY),
#                     skip_init_checks=True,
#                     additional_config=AdditionalConfig(
#                     timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
#                 ),
#             )
#             self.client.connect()
#             await self.ensure_collections_exist()
#             self.is_ready = True
#             print(f"Weaviate client ready: {self.client.is_ready()}")
#             return self.client
#         except Exception as e:
#             print(f"Error connecting to Weaviate: {str(e)}")
#             raise

#     async def ensure_collections_exist(self):
#         """Ensure required collections exist, create them if they don't."""
#         try:
#             collections = self.client.collections.list_all()
#             collection_names = [collection for collection in collections]

#             if TENANT_KNOWLEDGE_COLLECTION_NAME not in collection_names:
#                 print(f"Creating collection: {TENANT_KNOWLEDGE_COLLECTION_NAME}")
#                 # Create the collection with the specified settings
#                 self.client.collections.create(
#                     name=TENANT_KNOWLEDGE_COLLECTION_NAME,
#                     vectorizer_config=Configure.Vectorizer.text2vec_openai(
#                         model="text-embedding-3-small",
#                         base_url="https://api.openai.com",
#                         vectorize_collection_name=False,  # Equivalent to "Vectorize class name" being disabled
#                     ),
#                     properties=[
#                         Property(
#                             name="content", data_type=DataType.TEXT, vectorize=True
#                         ),
#                         Property(
#                             name="knowledge_type",
#                             data_type=DataType.TEXT,
#                             vectorize=False,
#                         ),
#                         Property(
#                             name="source", data_type=DataType.TEXT, vectorize=False
#                         ),
#                         Property(
#                             name="metadata",
#                             data_type=DataType.OBJECT,
#                             vectorize=False,
#                             nested_properties=[
#                                 Property(
#                                     name="source_id", data_type=DataType.TEXT, vectorize=False
#                                 ),
#                             ],
#                         ),
#                     ],
#                     multi_tenancy_config=Configure.multi_tenancy(
#                         enabled=True
#                     ),  # Multi-tenancy disabled
#                 )
#                 print(
#                     f"Collection {TENANT_KNOWLEDGE_COLLECTION_NAME} created successfully"
#                 )
#             else:
#                 print(f"Collection {TENANT_KNOWLEDGE_COLLECTION_NAME} already exists")

#         except Exception as e:
#             print(f"Error ensuring collections exist: {str(e)}")
#             raise

#     def close(self):
#         """Close the Weaviate client connection."""
#         if self.client:
#             self.client.close()
#             self.is_ready = False

#     def get_client(self):
#         """Return the Weaviate client instance."""
#         if not self.client:
#             while self.retry_count < MAX_RETRY_COUNT:
#                 try:
#                     self.connect()
#                     if self.client:
#                         break
#                 except Exception as e:
#                     self.retry_count += 1
#                     print(f"Error connecting to Weaviate: {str(e)}")
#             if not self.client:
#                 raise RuntimeError(
#                     "Weaviate client not initialized. Call connect() first."
#                 )
#         return self.client

# def initialize_weaviate_manager():
#     global weaviate_manager
#     weaviate_manager = WeaviateClientManager()
#     asyncio.run(weaviate_manager.connect())
#     sleep(2)
#     weaviate_manager.close()
#     return weaviate_manager

# # Dependency to get the Weaviate client
# def get_weaviate_client():
#     client = weaviate_manager.get_client()
#     print(client.is_ready())
#     if not client.is_ready():
#         print("Reconnecting to Weaviate")
#         weaviate_manager.connect()
#     return client
