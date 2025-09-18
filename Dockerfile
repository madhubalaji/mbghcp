FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 taskmanager && chown -R taskmanager:taskmanager /app
USER taskmanager

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=taskmanager.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "run.py"]