# Use a lightweight official Python image
FROM python:3.13-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy and install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code and set proper ownership
COPY --chown=appuser:appuser . .

# Switch to the non-root user
USER appuser

# Expose the port Uvicorn will run on
EXPOSE 8000

# Start Uvicorn (bind to 0.0.0.0 so it accepts external container traffic)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
