# Use Python 3.12-slim as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /chat_backend

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Set the default command to run the Django development server (for development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
