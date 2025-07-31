FROM python:3.12-slim as builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Configure uv
ENV PATH="/app/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app

# Install dependencies
COPY ./pyproject.toml ./uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy application code
COPY ./scripts /app/scripts
COPY ./app /app/app

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Final stage
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

CMD ["fastapi", "run", "--workers", "1", "app/main.py"]