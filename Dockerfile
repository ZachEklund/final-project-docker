FROM python:3.10

WORKDIR /app

# Copy requirements FIRST
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy backend
COPY src/ /app/

# Copy frontend
COPY frontend/ /app/frontend/

# Run FastAPI (Shell form to allow variable expansion)
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
