FROM python:3.13-slim

# Install packages and uv
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Add path
ENV PATH="/root/.local/bin:$PATH"

# Set workdir
WORKDIR /app

COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache --no-dev

# Copy files
COPY . .

# Expose port
EXPOSE 8000

# Run via uvicorn
CMD ["uv", "run", "uvicorn", "rate_owl.main:app", "--host", "0.0.0.0", "--port", "8000"]