# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install system dependencies (if needed) and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port for Flask
EXPOSE 5000

# Optional: set environment variables for LLM (replace with .env in production)
# ENV LLM_PROVIDER=ollama
# ENV AZURE_API_KEY=your_api_key_here

# Run the Flask app
CMD ["python", "app.py"]
