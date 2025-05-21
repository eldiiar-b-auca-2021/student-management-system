# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (optional if using whitenoise)
# RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "student_project.wsgi:application", "--bind", "0.0.0.0:8000"]
