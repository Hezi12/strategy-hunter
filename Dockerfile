# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY web/requirements.txt web/
RUN pip install --no-cache-dir -r web/requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p web/static web/templates

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=web/app.py
ENV FLASK_ENV=production
ENV PORT=5001

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/ || exit 1

# Run the web application
CMD ["python3", "web/app.py"] 