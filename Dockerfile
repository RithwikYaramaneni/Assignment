# Stage 1: Light Python Base Image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output for real-time logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies separately for layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py /app/

# Create a non-root user for container security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Entry command to run application
CMD ["python", "app.py"]