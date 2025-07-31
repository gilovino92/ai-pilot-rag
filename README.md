# AI Pilot RAG

A Retrieval-Augmented Generation (RAG) system built with FastAPI that provides intelligent knowledge retrieval and AI-powered responses. This service integrates with vector databases (Weaviate), AI providers (OpenAI/AWS Bedrock), and supports document processing for enhanced knowledge management.

## Features

- **Vector Search**: Powered by Weaviate for semantic document retrieval
- **AI Integration**: Support for OpenAI and AWS Bedrock models
- **Document Processing**: Handle PDF, DOCX, and Excel files
- **Multi-tenant**: Tenant-specific knowledge collections
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **PostgreSQL**: Robust data persistence
- **Authentication**: API key-based security

## Prerequisites

- Python 3.10+ ([Download](https://www.python.org/downloads/))
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- PostgreSQL database
- Weaviate instance
- AI provider API keys (OpenAI or AWS)

## Setup & Run

### Using uv (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-pilot-rag
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Environment setup**:
   ```bash
   cp .env.template .env
   # Edit .env with your configuration values
   ```

4. **Run the application**:
   ```bash
   uv run uvicorn app.main:app --reload --port 8320
   ```

### Using pip

1. **Clone and setup virtual environment**:
   ```bash
   git clone <repository-url>
   cd ai-pilot-rag
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Environment setup**:
   ```bash
   cp .env.template .env
   # Edit .env with your configuration values
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --port 8320
   ```

## Configuration

Required environment variables in `.env`:

### Core Settings
- `ENVIRONMENT`: Development environment (local/dev/prod)
- `PROJECT_NAME`: Name of your project
- `PORT`: Application port (default: 8320)
- `SECRET_KEY`: Application secret key
- `API_KEY`: API key for authentication

### Database
- `POSTGRES_SERVER`: PostgreSQL server host
- `POSTGRES_PORT`: PostgreSQL port
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password

### Vector Database
- `WEAVIATE_URL`: Weaviate instance URL
- `WEAVIATE_API_KEY`: Weaviate API key

### AI Provider
- `AI_AGENT_PROVIDER`: AI provider (openai/bedrock)
- `EMBEDDING_MODEL`: Embedding model to use
- `AWS_ACCESS_KEY_ID`: AWS access key (if using Bedrock)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (if using Bedrock)
- `AWS_REGION`: AWS region (if using Bedrock)

### Collections
- `GENERAL_KNOWLEDGE_COLLECTION_NAME`: General knowledge collection
- `TENANT_KNOWLEDGE_COLLECTION_NAME`: Tenant-specific collection

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8320/docs`
- **ReDoc**: `http://localhost:8320/redoc`

## Development

### Code Quality
```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Type checking
uv run mypy .
```

### Scripts
- `scripts/format.sh`: Format code
- `scripts/lint.sh`: Run linting
- `scripts/test.sh`: Run tests
- `scripts/prestart.sh`: Pre-start setup

## Docker

```bash
# Build image
docker build -t ai-pilot-rag .

# Run container
docker run -p 8320:8320 --env-file .env ai-pilot-rag
```

## Troubleshooting

- **Python version**: Ensure Python 3.10+ is installed
- **Dependencies**: Run `uv sync` or `pip install -e .` to install/update dependencies
- **Database connection**: Verify PostgreSQL is running and credentials are correct
- **Weaviate connection**: Ensure Weaviate instance is accessible
- **Environment variables**: Check all required variables are set in `.env`