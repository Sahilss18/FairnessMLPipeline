FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create runtime directories
RUN mkdir -p models embeddings outputs data

# Copy source code and api
COPY src/ ./src/
COPY api/ ./api/

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

EXPOSE 5000

CMD ["python", "api/app.py"]

