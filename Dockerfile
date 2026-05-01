# Use a slim Python 3.12 image
FROM python:3.12-slim-bookworm

# Install system dependencies for Tesseract OCR (required by pytesseract)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation and optimization
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (excluding development tools)
RUN uv sync --frozen --no-install-project --no-dev

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the FastAPI application using uv to ensure the virtualenv is correctly managed
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]