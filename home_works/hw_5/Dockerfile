# Dockerfile
# To build and run the container:
# docker build -t fastapi-app .
# docker run -p 8000:8000 fastapi-app

# Use a minimal Python 3.10 image to reduce the size of the container and improve performance
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for the application
EXPOSE 8000

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
