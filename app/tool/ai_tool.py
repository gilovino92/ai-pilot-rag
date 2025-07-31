from typing import Dict, List, Optional
from app.core.ai_agents.factory import AIAgentFactory
from app.core.config import settings
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

# Get the configured AI agent provider
agent_provider = settings.AI_AGENT_PROVIDER  # Will be "openai" or "ai_tool"

# Get the configured embedding model
embedding_model = (
    settings.EMBEDDING_MODEL
)  # Will be "text-embedding-ada-002" by default


class AITool:
    def __init__(self):
        self.ai_agent = AIAgentFactory.create_agent(agent_provider)
        self.client = self.ai_agent.get_client()

    async def get_completion(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Get a completion from OpenAI's API.

        Args:
            prompt: The input prompt
            model: The model to use (default: gpt-3.5-turbo)
            temperature: The temperature for response generation (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate

        Returns:
            The generated completion text
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting completion from OpenAI: {str(e)}")

    async def get_embeddings(
        self,
        text: str,
        model: str = embedding_model,
    ) -> List[float]:
        """
        Get embeddings for a text using OpenAI's API.

        Args:
            text: The input text to get embeddings for
            model: The model to use (default: text-embedding-ada-002)

        Returns:
            List of embedding values
        """
        try:
            response =  self.client.embeddings.create(
                model=model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error getting embeddings from OpenAI: {str(e)}")

    async def get_embeddings_batch(
        self,
        texts: List[str],
        model: str = embedding_model,
    ) -> List[List[float]]:
        """
        Get embeddings for multiple texts using OpenAI's API.

        Args:
            texts: List of input texts to get embeddings for
            model: The model to use (default: text-embedding-ada-002)

        Returns:
            List of embedding lists
        """
        try:
            response = await self.client.embeddings.create(
                model=model,
                input=texts,
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"Error getting batch embeddings from OpenAI: {str(e)}")

    async def generate_sql_query(
        self,
        user_query: str,
        tables_info: str,
        db_dialect: str,
        top_k: int = 5,
    ) -> str:
        """
        Generate a SQL query based on user question and table information.

        Args:
            user_query: The user's question
            tables_info: Information about available tables and their columns
            db_dialect: The SQL dialect to use (e.g., 'postgresql', 'mysql')
            top_k: Maximum number of results to return (default: 5)

        Returns:
            Generated SQL query as a string
        """
        prompt = f"""Given an input question, create a syntactically correct {db_dialect} query to run to help find the answer.Unless the user specifies in his question a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database. Never query for all the columns from a specific table, only ask for a the few relevant columns given the question. Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Only use the following these tables:{tables_info}. Question: {user_query}."""
        try:
            response =  self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": str(prompt)}],  # Ensure prompt is string
                temperature=0.0,  # Use 0 temperature for deterministic SQL generation
            )
            return str(response.choices[0].message.content).strip()  # Ensure return value is string
        except Exception as e:
            raise Exception(f"Error generating SQL query: {str(e)}")
        
ai_tool = AITool();
def get_ai_tool():
    """Return the AI tool instance."""
    return ai_tool



