# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
RUN rm -f .env /app/data/session.json
RUN rm -f /app/data/follows.json
RUN rm -f /app/data/timeline.json

# Run the bot
CMD ["python", "index.py"] 