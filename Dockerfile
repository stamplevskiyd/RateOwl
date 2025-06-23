########################################
# Build stage: frontend
########################################
FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend .
RUN npm run build

########################################
# Build stage: backend
########################################
FROM python:3.13-slim AS backend

# Install uv and build deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Poetry/uv deps
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev

# Copy backend source
COPY . .

# Copy compiled frontend assets into static directory
COPY --from=frontend-build /frontend/dist ./static

EXPOSE 8000

CMD ["/app/scripts/run_app.sh"]
