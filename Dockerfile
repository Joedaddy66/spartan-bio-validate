# Use Python 3.12 for maximum performance
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     gcc     python3-dev     && rm -rf /var/lib/apt/lib/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the engine
COPY . .

# Expose the Bureau port
EXPOSE 8001

# Ignition
CMD ["python", "main.py"]
