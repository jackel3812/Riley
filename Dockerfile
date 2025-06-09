# Use slim Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy core application files
COPY requirements.txt .
COPY app.py .
COPY Procfile .
COPY runtime.txt .
COPY railway.toml .

# Copy essential Riley components
COPY jarvis/ ./jarvis/
COPY static/ ./static/
COPY templates/ ./templates/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Cleanup unnecessary files
RUN find . -type d -name "__pycache__" -exec rm -r {} + && \
    find . -type f -name "*.pyc" -delete && \
    find . -type f -name "*.pyo" -delete

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Expose port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
