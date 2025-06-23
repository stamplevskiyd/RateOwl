FROM python:3.13-slim


RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "owl_core.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]