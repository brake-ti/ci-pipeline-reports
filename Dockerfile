# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install dependencies from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels && \
    rm -rf /root/.cache/pip

# Setup logging directory
RUN mkdir -p /var/log && \
    touch /var/log/app.log && \
    chown -R appuser:appuser /var/log/app.log

# Copy application code
COPY src /app/src
COPY VERSION /app/VERSION

# Switch to non-root user
USER appuser

# Healthcheck (Python native to avoid installing curl)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; import os; port = os.getenv('PORT', 8000); urllib.request.urlopen(f'http://localhost:{port}/health/live')" || exit 1

EXPOSE ${PORT}

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT} --workers 1 --loop uvloop"]
