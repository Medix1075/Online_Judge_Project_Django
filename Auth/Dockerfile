# Use official Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && apt-get install -y gcc g++ libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy only requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy minimal project files required to run Compiler
COPY manage.py .
COPY Auth/settings.py Auth/urls.py Auth/__init__.py Auth/wsgi.py ./Auth/
COPY Compiler ./Compiler
COPY authentication ./authentication
COPY Problems ./Problems
COPY templates ./templates
COPY .env .

RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
