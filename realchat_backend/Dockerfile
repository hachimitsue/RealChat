FROM python:3.9-slim

WORKDIR /app

# Install dependencies (including gunicorn)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Create directories for database and static files
RUN mkdir -p /app/db_data
RUN mkdir -p /app/staticfiles

# Copy the entire backend project
COPY . /app/

# Ensure entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=/app/staticfiles

EXPOSE 8000

CMD ["/app/entrypoint.sh"]