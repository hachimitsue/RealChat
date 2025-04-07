FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Create directory for SQLite database
RUN mkdir -p /app/db_data

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Copy project
COPY . /app/

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=/app/staticfiles

# Expose port
EXPOSE 8000

# Run entrypoint script
CMD ["/app/entrypoint.sh"]