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

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=/app/staticfiles

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "realchat.wsgi:application", "--bind", "0.0.0.0:8000"]