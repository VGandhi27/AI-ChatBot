# Use Python 3.12-slim as the base image
FROM python:3.12-slim

# Set the working directory inside container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project
COPY . .

# Expose Django port
EXPOSE 8000

# Default command to run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
